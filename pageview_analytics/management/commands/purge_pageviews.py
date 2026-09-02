"""Retention cleanup. Much simpler than the PHP original's purge-analytics.php:
that script existed to reconcile a maintained JSON aggregate against what it
was purging from a rolling log -- two numbers that could drift apart. Here
there is no separate aggregate; a DELETE just is correct, nothing to
reconcile."""
import ipaddress

from django.core.management.base import BaseCommand
from django.utils import timezone

from pageview_analytics.models import PageView, VisitorLocation


class Command(BaseCommand):
    help = 'Delete page views matching the given filters (retention, spot cleanup).'

    def add_arguments(self, parser):
        parser.add_argument('--older-than', type=int, help='Delete views older than N days.')
        parser.add_argument('--ip', help='Delete views from this address or CIDR range.')
        parser.add_argument('--datacentres', action='store_true', help='Delete views from datacentre networks.')
        parser.add_argument('--dry-run', action='store_true', help='Show what would be deleted, change nothing.')

    def handle(self, *args, older_than=None, ip=None, datacentres=False, dry_run=False, **kwargs):
        qs = PageView.objects.all()

        if older_than is not None:
            cutoff = timezone.now() - timezone.timedelta(days=older_than)
            qs = qs.filter(created_at__lt=cutoff)

        if ip:
            network = ipaddress.ip_network(ip, strict=False)
            matching_ids = [
                loc.id for loc in VisitorLocation.objects.all()
                if ipaddress.ip_address(loc.ip_address) in network
            ]
            qs = qs.filter(location_id__in=matching_ids)

        if datacentres:
            dc_ids = [loc.id for loc in VisitorLocation.objects.all() if loc.is_datacenter()]
            qs = qs.filter(location_id__in=dc_ids)

        if older_than is None and not ip and not datacentres:
            self.stdout.write(self.style.WARNING('No filters given -- nothing to do. See --help.'))
            return

        count = qs.count()
        if dry_run:
            self.stdout.write(f'Would delete {count} page view(s).')
            return

        qs.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} page view(s).'))
