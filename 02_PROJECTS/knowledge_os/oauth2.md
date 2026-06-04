---
knowledge_os_machine_key: oauth2
knowledge_os_domain: APIs & Protocols
knowledge_os_status: Not Started
knowledge_os_score: 0
knowledge_os_priority: Medium
---
# OAuth2

## What It Is
OAuth2 is the standard that lets one application access your data in another
service without ever seeing your password. When an app asks to connect to your
Google account, OAuth2 is what lets you grant it limited access, Google verifies
you, and the app gets a token to act on your behalf, never your actual
credentials. It is delegated access: permission without password-sharing.

## How It Works
The flow runs through the service that holds your account. The app redirects you to
that service, where you log in directly, the app never sees this, and approve a
specific scope of access. The service then hands the app an access token, a
time-limited credential representing exactly the permission you granted. The app
uses that token on its API calls to prove it is allowed, and when the token
expires, a refresh token lets it quietly get a new one without asking you again.
The key separation is that authentication, proving who you are, happens with the
service you trust, while the app only ever receives a scoped, revocable token.

## Why It Matters
OAuth2 solves a real danger: handing your password to a third-party app would give
it total, permanent access to your account. Tokens are better in every way, they
are scoped to specific permissions, they expire, and you can revoke them without
changing your password. This is why connecting services, your Google Drive to a
backend, your account to an integration, uses OAuth2 tokens stored as credentials
rather than embedded passwords. Understanding it explains why those token files
exist and why protecting them matters as much as protecting a password.

## The Pattern
Grant scoped, revocable, expiring tokens instead of sharing passwords.
Authentication stays with the trusted service; the app gets only the limited access
you approved.
