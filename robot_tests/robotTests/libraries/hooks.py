from robot.api import ExecutionResult
import sendgrid
import os
from sendgrid.helpers.mail import *
from slacker import Slacker

ROBOT_LISTENER_API_VERSION = 2

tests = []


def end_test(self, data):

    name = self
    status = data['status']
    elapsed_time = data['elapsedtime']
    body = """Test: {} {} {}""".format(name, status, elapsed_time)
    tests.append(body)


def output_file(path):
    """
    Once the output file is ready with the results. Those are sended via email and slack
    :param path:
    """
    result = ExecutionResult(path)
    result.configure(stat_config={'suite_stat_level': 2,
                                  'tag_stat_combine': 'tagANDanother'})

    # Email section
    # Append the tests results
    stats = result.statistics
    summary_tests = []
    for stat in stats.suite:
        test_passed = "succeeded"
        if stat.passed == 0:
            test_passed = "Failed"
        result = stat.name + ": " + test_passed
        summary_tests.append(result)

    # gets passed, failed and combined results
    tests_failed = stats.total.critical.failed
    tests_passed = stats.total.critical.passed
    tests_combined = stats.tags.combined[0].total
    summary = "Test summary:<br>"
    summary += "<br>".join(summary_tests)
    summary += """ <br>
                Critical tests failed: {}<br>
                Critical tests passed: {}<br>
                Critical tests combined: {}<br>
    """.format(tests_failed, tests_passed, tests_combined)

    body = "<br>"
    body += summary
    send_email(body)

    # Slack section
    body_tests_slack = "Tests: \n"
    body_tests_slack += "\n".join(tests)

    summary_slack = "Test summary:"
    summary_slack += """
                Critical tests failed: {}
                Critical tests passed: {}
                Critical tests combined: {}
    """.format(tests_failed, tests_passed, tests_combined)

    print(os.environ.get('SLACK_TOKEN'))
    slack = Slacker(os.environ.get('SLACK_TOKEN'))
    channel = slack.channels.get_channel_id(channel_name="robot_tests")
    slack.chat.post_message(channel=channel, text=summary_slack)
    slack.chat.post_message(channel=channel, text=body_tests_slack)


def send_email(body):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("andres.haskel@innuy.com")
    to_email = Email("andres.haskel@innuy.com")
    subject = "Sending with SendGrid is Fun"
    content = Content("text/html", body)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)