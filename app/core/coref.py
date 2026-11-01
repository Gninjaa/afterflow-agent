import logging

from app.core.llm import get_chat_model
from app.core.prompts import COREF_REWRITE_PROMPT

logger = logging.getLogger(__name__)


async def resolve(
    query: str, history: str = "", *, conversation_id: int | None = None
) -> str:
    """指代消解 + 口语归一。结合历史把半截话补成完整问句;已完整则原样。
    出错兜底:返回原句(不阻断下游)。"""
    try:
        model = get_chat_model()
        r = await (COREF_REWRITE_PROMPT | model).ainvoke(
            {"query": query, "history": history or "(无)"})
        text = (r.content if isinstance(r.content, str) else "").strip()
    except Exception:
        logger.exception("指代消解失败，回退到用户原话 conv=%s", conversation_id)
        return query
    return text or query
