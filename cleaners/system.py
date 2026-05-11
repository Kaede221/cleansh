"""系统级清理：dnf 包缓存 / autoremove、systemd 日志（需 sudo）"""

from rich.prompt import Confirm

from ._common import console, has, run, skip


def clean_dnf() -> None:
    if not has("dnf"):
        skip("dnf")
        return
    # 涉及 sudo 且 autoremove 会卸载未被依赖的包，二次确认
    if not Confirm.ask(
        "将执行 sudo dnf autoremove / clean all（会卸载孤立包并清除包缓存），确认继续？",
        default=False,
    ):
        console.print("[yellow]已跳过 dnf 清理[/yellow]")
        return
    run("sudo dnf autoremove -y")
    run("sudo dnf clean all")


def clean_journal() -> None:
    if not has("journalctl"):
        skip("journalctl")
        return
    # 删除的是系统日志，影响后续问题排查，二次确认
    if not Confirm.ask(
        "将清理 systemd 日志，仅保留最近 7 天（sudo journalctl --vacuum-time=7d），确认继续？",
        default=False,
    ):
        console.print("[yellow]已跳过 journal 清理[/yellow]")
        return
    run("sudo journalctl --vacuum-time=7d")
