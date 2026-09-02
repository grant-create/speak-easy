"""Bot/network filtering -- two independent layers, both applied before a
visit is ever recorded (see tracking.track_visit)."""
import ipaddress

from pageview_analytics import config

# Blunt on purpose: one pass over a short substring list, case-insensitive,
# catches the great majority of crawler/monitor noise cheaply. It will never
# be perfect against a determined scraper spoofing a browser UA -- that's
# what the "no JS" signal in the dashboard is for instead.
BOT_PATTERNS = (
    'bot', 'crawl', 'spider', 'slurp', 'facebookexternalhit',
    'preview', 'monitor', 'uptime', 'curl', 'wget', 'python-requests',
    'scanner', 'headless', 'fetch', 'archive.org_bot', 'ia_archiver',
    'semrush', 'ahrefs', 'mj12', 'dotbot', 'petalbot', 'bytespider',
    'gptbot', 'ccbot', 'claudebot', 'perplexity', 'applebot',
    'phantomjs', 'selenium', 'puppeteer', 'playwright',
    'go-http-client', 'java/', 'okhttp', 'libwww', 'httpclient',
    'axios', 'node-fetch', 'postman', 'insomnia', 'lighthouse',
    'pingdom', 'statuscake', 'newrelic', 'datadog', 'zgrab', 'masscan',
    # Uptime/load-balancer health checks -- these poll every few seconds
    # forever and would otherwise dwarf real traffic.
    'health', 'route53', 'route 53', 'amazonaws', 'cloudfront',
    'site24x7', 'nagios', 'zabbix', 'checkly', 'hetrix', 'updown.io',
    'uptimerobot', 'statuspage', 'prtg', 'icinga', 'sensu', 'telegraf',
)


def is_bot(user_agent):
    if not user_agent:
        return True
    ua = user_agent.lower()
    return any(pattern in ua for pattern in BOT_PATTERNS)


def is_ignored_ip(ip_address):
    """Backstop for when a client lies about its user agent: anything from
    a named network is never counted, whatever it claims to be."""
    try:
        ip = ipaddress.ip_address(ip_address)
    except ValueError:
        return False

    for entry in config.get('IGNORE_NETWORKS'):
        entry = entry.strip()
        if not entry:
            continue
        try:
            if '/' in entry:
                if ip in ipaddress.ip_network(entry, strict=False):
                    return True
            elif ip == ipaddress.ip_address(entry):
                return True
        except ValueError:
            continue

    return False
