"""Keep an LLM's proposed email action behind deterministic policy checks."""

from dataclasses import dataclass


class PolicyDenied(Exception):
    pass


@dataclass(frozen=True)
class UserContext:
    user_id: str
    organization_domain: str
    scopes: frozenset[str]


@dataclass(frozen=True)
class ProposedEmail:
    recipient: str
    subject: str
    body: str
    body_classification: str
    attachment_ids: tuple[str, ...]


def authorize_email(
    user: UserContext,
    proposal: ProposedEmail,
    *,
    attachment_classification: dict[str, str],
    user_confirmed_exact_action: bool,
) -> None:
    """Raise before a send tool is called when any hard rule fails."""
    if "email:send" not in user.scopes:
        raise PolicyDenied("the authenticated user cannot send email")

    recipient_domain = proposal.recipient.rsplit("@", 1)[-1].lower()
    sends_outside_org = recipient_domain != user.organization_domain.lower()
    classifications = [proposal.body_classification]
    for file_id in proposal.attachment_ids:
        classification = attachment_classification.get(file_id)
        if classification is None:
            raise PolicyDenied(f"attachment {file_id} has no classification")
        classifications.append(classification)

    if sends_outside_org and "confidential" in classifications:
        raise PolicyDenied("confidential content cannot leave the organization")
    if not user_confirmed_exact_action:
        raise PolicyDenied("show the recipient and attachments, then request confirmation")


def _send_with_narrow_client(user: UserContext, proposal: ProposedEmail) -> None:
    """Placeholder for the private, narrowly credentialed email API client."""
    print(f"sending '{proposal.subject}' to {proposal.recipient} as {user.user_id}")


def send_guarded_email(
    user: UserContext,
    proposal: ProposedEmail,
    *,
    attachment_classification: dict[str, str],
    user_confirmed_exact_action: bool,
) -> None:
    """The only public send path authorizes the complete outbound payload first."""
    authorize_email(
        user,
        proposal,
        attachment_classification=attachment_classification,
        user_confirmed_exact_action=user_confirmed_exact_action,
    )
    _send_with_narrow_client(user, proposal)


# The model may propose an action. It cannot gain a scope, choose an unclassified
# attachment, or reach the private send client through this tool boundary.
