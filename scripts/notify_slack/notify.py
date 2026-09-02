"""JUnit XML(pytest --junitxml 산출물)을 파싱해 실패한 테스트를 Slack Incoming Webhook으로
알린다.

Source of Truth: docs/automation/AUTOMATION_GUIDE.md 16절(Slack Notification 원칙),
CLAUDE.md 16절(Slack은 CI 결과 알림 전용, Commit/Push 승인 용도 아님), 17절(Secret은
GitHub Secrets/환경변수로만 관리, 하드코딩 금지)
- 성공(실패 0건) 시에는 알림을 보내지 않는다(실패 시 전용).
- 표준 라이브러리(xml.etree.ElementTree, urllib.request)만 사용하며 3rd-party 패키지에
  의존하지 않는다(최소 의존성 원칙).
"""

import json
import logging
import os
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

DEFAULT_JUNIT_XML_PATH = "automation/reports/results.xml"
MAX_LISTED_FAILURES = 10
MAX_MESSAGE_LENGTH = 200


def parse_junit_xml(path: str) -> dict:
    """JUnit XML을 파싱해 총 테스트 수/실패 수/실패 목록(테스트명, 사유 요약)을 반환한다."""
    tree = ET.parse(path)
    root = tree.getroot()
    suite = root if root.tag == "testsuite" else root.find("testsuite")
    if suite is None:
        raise ValueError(f"{path}에서 testsuite 엘리먼트를 찾을 수 없습니다")

    failures = []
    for testcase in suite.iter("testcase"):
        failure_el = testcase.find("failure")
        error_el = testcase.find("error")
        node = failure_el if failure_el is not None else error_el
        if node is not None:
            message = (node.get("message") or "").replace("\n", " ")
            failures.append(
                {
                    "name": f"{testcase.get('classname')}::{testcase.get('name')}",
                    "message": message[:MAX_MESSAGE_LENGTH],
                }
            )

    return {
        "total": int(suite.get("tests", 0)),
        "failed": int(suite.get("failures", 0)) + int(suite.get("errors", 0)),
        "failures": failures,
    }


def build_slack_message(summary: dict) -> dict:
    """Slack Incoming Webhook payload를 구성한다."""
    lines = [f"*QA 자동화 테스트 실패*: {summary['failed']}/{summary['total']}건 실패"]
    for failure in summary["failures"][:MAX_LISTED_FAILURES]:
        lines.append(f"- `{failure['name']}`: {failure['message']}")
    remaining = summary["failed"] - len(summary["failures"][:MAX_LISTED_FAILURES])
    if remaining > 0:
        lines.append(f"...외 {remaining}건")
    return {"text": "\n".join(lines)}


def send_to_slack(webhook_url: str, payload: dict) -> None:
    """Slack Incoming Webhook으로 payload를 전송한다."""
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        webhook_url, data=data, headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(request, timeout=10)
    except urllib.error.URLError as exc:
        logger.error("Slack Webhook 전송 실패: %s", exc)
        raise


def main() -> None:
    junit_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_JUNIT_XML_PATH
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        raise RuntimeError("SLACK_WEBHOOK_URL 환경변수가 설정되지 않았습니다")

    summary = parse_junit_xml(junit_path)
    if summary["failed"] == 0:
        logger.info("실패한 테스트가 없어 Slack 알림을 보내지 않습니다")
        return

    send_to_slack(webhook_url, build_slack_message(summary))
    logger.info("Slack 알림 전송 완료 (%d/%d건 실패)", summary["failed"], summary["total"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
