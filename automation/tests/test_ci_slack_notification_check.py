"""[임시 파일] Phase Final Task 5 - GitHub Actions Slack 알림 실제 도착 여부 확인용.

실제 TC(docs/tc/*.md)와 무관하며, `.github/workflows/ci.yml`의 Slack 알림 스텝이
테스트 실패 시 실제로 Slack Webhook까지 메시지를 전송하는지 1회 확인하기 위한 목적으로만
존재한다. 확인이 끝나면 이 파일은 즉시 삭제하고 커밋한다(사용자 승인 완료).
"""


def test_intentional_failure_for_slack_notification_check():
    """의도적으로 실패시켜 Slack 알림 전송 경로를 실제로 검증하기 위한 테스트."""
    assert False, "Phase Final Slack 알림 실제 도착 확인용 의도적 실패 (임시 테스트)"
