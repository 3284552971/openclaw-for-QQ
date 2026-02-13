import json
import os

from ncatbot.core import BotClient, GroupMessage, PrivateMessage
from ncatbot.utils import get_log

bot = BotClient()
_log = get_log()

ROOT_ID = os.getenv("NCATBOT_ROOT_ID", "1000000001")
BOT_UIN = os.getenv("NCATBOT_BOT_UIN", "1000000002")


def _load_commands():
    default_commands = {
        "task_dict": {
            "#帮助": "可用命令: #重载",
        },
        "transfer": {},
        "root_transfer": {},
    }
    try:
        with open("commands.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return default_commands
        data.setdefault("task_dict", default_commands["task_dict"])
        data.setdefault("transfer", default_commands["transfer"])
        data.setdefault("root_transfer", default_commands["root_transfer"])
        return data
    except Exception:
        return default_commands


COMMANDS = _load_commands()


async def _reload_official_openclaw_plugin():
    loader = getattr(bot, "plugin_loader", None)
    if loader is None:
        return False, "插件系统未就绪"
    try:
        if "openclaw" in loader.plugins:
            ok = await loader.reload_plugin("openclaw")
            return bool(ok), "openclaw 重载成功" if ok else "openclaw 重载失败"
        plugin = await loader.load_plugin("openclaw")
        ok = plugin is not None
        return ok, "openclaw 加载成功" if ok else "openclaw 加载失败"
    except Exception as exc:
        return False, str(exc)


@bot.group_event()
async def on_group_message(msg: GroupMessage):
    _log.info(msg)
    message = (msg.raw_message or "").strip()
    mention_tag = f"[CQ:at,qq={BOT_UIN}]"
    clean = message.replace(f"{mention_tag} ", "").replace(mention_tag, "").strip()

    # root 管理命令：重载 openclaw
    if str(msg.user_id) == ROOT_ID and clean.startswith("#重载"):
        global COMMANDS
        COMMANDS = _load_commands()
        ok, detail = await _reload_official_openclaw_plugin()
        await msg.reply(text=("重载成功" if ok else f"重载失败: {detail}"), at=msg.user_id)
        return

    # 其余 # 命令仅做提示（openclaw 自身触发靠 @机器人 或 root 私聊）
    if clean.startswith("#"):
        task_text = COMMANDS.get("task_dict", {}).get(clean)
        if task_text:
            await msg.reply(text=str(task_text), at=msg.user_id)
        elif str(msg.user_id) == ROOT_ID and clean in {"#openclaw", "#oc"}:
            await msg.reply(text="openclaw 官方插件已加载，群聊请直接 @机器人 提问。", at=msg.user_id)
        else:
            await msg.reply(text="请 @机器人 后直接提问，或使用 #重载。", at=msg.user_id)


@bot.private_event()
async def on_private_message(msg: PrivateMessage):
    _log.info(msg)
    # root 私聊由 openclaw 插件接管
    if str(msg.user_id) == ROOT_ID:
        return

    # 非 root 私聊提示
    await bot.api.post_private_msg(msg.user_id, text="当前示例仅开放 root 私聊；群聊请 @机器人 使用。")


if __name__ == "__main__":
    bot.run(bt_uin=BOT_UIN)
