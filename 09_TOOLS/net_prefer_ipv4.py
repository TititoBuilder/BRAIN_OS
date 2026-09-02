"""
category: library
net_prefer_ipv4.py — Force IPv4 for outbound requests in this process.

Verified 2026-09-01: 20 one-shot processes against huggingface.co, default
resolution failed 2 of 10 with WinError 10054; forced IPv4 failed 0 of 10.
api.telegram.org and huggingface.co both resolve IPv6-first from this
machine; api.github.com does not and never exhibited the failure.

This is the root cause of the intermittent WinError 10054 in Telegram sends,
which timeout, concurrency, token, and network checks all failed to explain.
Each vault tool makes one request and exits, so a per-process first-connection
failure looks random from the outside.

Import for the side effect, before any outbound call:
    import net_prefer_ipv4  # noqa: F401

Self-test:
    python C:/BRAIN_OS/09_TOOLS/net_prefer_ipv4.py
"""

import socket

_original_getaddrinfo = socket.getaddrinfo


def _ipv4_only(host, port, family=0, *args, **kwargs):
    return _original_getaddrinfo(host, port, socket.AF_INET, *args, **kwargs)


def enable() -> None:
    """Restrict resolution to IPv4 for the remainder of this process."""
    socket.getaddrinfo = _ipv4_only


def disable() -> None:
    """Restore the original resolver."""
    socket.getaddrinfo = _original_getaddrinfo


enable()


if __name__ == "__main__":
    for host in ("api.telegram.org", "huggingface.co", "api.github.com"):
        addrs = [a[4][0] for a in socket.getaddrinfo(host, 443)]
        print(f"{host:22} {addrs}")
