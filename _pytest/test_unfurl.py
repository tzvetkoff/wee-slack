from __future__ import print_function, unicode_literals

import wee_slack
import pytest


@pytest.mark.parametrize('case', (
    {
        'input': "foo",
        'output': "foo",
    },
    {
        'input': "<!channel>",
        'output': "@channel",
    },
    {
        'input': "<!everyone>",
        'output': "@everyone",
    },
    {
        'input': "<!group>",
        'output': "@group",
    },
    {
        'input': "<!here>",
        'output': "@here",
    },
    {
        'input': "<@U407ABLLW|@othernick>: foo",
        'output': "@alice: foo",
    },
    {
        'input': "<@UNKNOWN|@othernick>: foo",
        'output': "@othernick: foo",
    },
    {
        'input': "foo <#C407ABS94|otherchannel> foo",
        'output': "foo #general foo",
    },
    {
        'input': "foo <#UNKNOWN|otherchannel> foo",
        'output': "foo #otherchannel foo",
    },
    {
        'input': "url: <https://example.com|fallback> suffix",
        'output': "url: https://example.com suffix",
        'ignore_alt_text': True,
    },
    {
        'input': "url: <https://example.com|example> suffix",
        'output': "url: https://example.com (example) suffix",
        'auto_link_display': 'both',
    },
    {
        'input': "url: <https://example.com|example with spaces> suffix",
        'output': "url: https://example.com (example with spaces) suffix",
        'auto_link_display': 'both',
    },
    {
        'input': "url: <https://example.com|example.com> suffix",
        'output': "url: https://example.com (example.com) suffix",
        'auto_link_display': 'both',
    },
    {
        'input': "url: <https://example.com|example.com> suffix",
        'output': "url: example.com suffix",
        'auto_link_display': 'text',
    },
    {
        'input': "url: <https://example.com|different text> suffix",
        'output': "url: https://example.com (different text) suffix",
        'auto_link_display': 'text',
    },
    {
        'input': "url: <https://example.com|different text> suffix",
        'output': "url: https://example.com (different text) suffix",
        'auto_link_display': 'url',
    },
    {
        'input': "url: <https://example.com|example.com> suffix",
        'output': "url: https://example.com suffix",
        'auto_link_display': 'url',
    },
    {
        'input': "<@U407ABLLW> multiple unfurl <https://example.com|example with spaces>",
        'output': "@alice multiple unfurl https://example.com (example with spaces)",
        'auto_link_display': 'both',
    },
    {
        'input': "try the #general channel",
        'output': "try the #general channel",
    },
    {
        'input': "<@U407ABLLW> I think 3 > 2",
        'output': "@alice I think 3 > 2",
    },
    {
        'input': "<!subteam^TGX0ALBK3|@othersubteam> This is announcement for the dev team",
        'output': "@test This is announcement for the dev team"
    },
    {
        'input': "<!subteam^UNKNOWN|@othersubteam> This is announcement for the dev team",
        'output': "@othersubteam This is announcement for the dev team"
    },
    {
        'input': "Ends <!date^1584573568^{date_short} at {time}|Mar 18, 2020 at 23:19 PM>.",
        'output': "Ends Mar 18, 2020 at 23:19 PM."
    }
))
def test_unfurl_refs(case, realish_eventrouter):
    wee_slack.EVENTROUTER = realish_eventrouter
    wee_slack.config.unfurl_ignore_alt_text = case.get('ignore_alt_text')
    wee_slack.config.unfurl_auto_link_display = case.get('auto_link_display')

    result = wee_slack.unfurl_refs(case['input'])
    assert result == case['output']
