from django.utils.timezone import now
from datetime import datetime, timezone
import pytz
from django.db import models
# from osm_field.fields import OSMField, LatitudeField, LongitudeField
# from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _  # lazy needed in models
from django.core.validators import MinValueValidator, MaxValueValidator


from django.contrib.auth.models import AbstractUser, Group, Permission
import random
import string
import os
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from timezone_field import TimeZoneField
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta, timezone

#from owner.models import PoolOwner
#from poolbuilder.models import PoolBuilder




PUMP_SPEEDS = [
    (0, _("Off")),
    (1, _("Low")),
    (2, _("Medium")),
    (3, _("High")),
    (4, _("Maximum"))
]

PH_CHOICES = [
    (0, "pH+"),
    (1, "pH-"),
    (2, "pH+ & pH-")
]

LANGUAGES = [
    (0, "Nederlands"),
    (1, "English"),
    (2, "Deutsch"),
    (2, "Français")
]

LANGUAGES_CODE = [
    (0, "nl"),
    (1, "en"),
    (2, "de"),
    (2, "fr")
]

ALARM_CHOICES = [
    (0, "N/O"),
    (1, "N/C")
]

EXTOFF_CHOICES = [
    (0, "Off"),
    (1, "N/O"),
    (2, "N/C")
]

PUMP_VOLUME = [
    (0, "1.5 l/h"),
    (1, "3 l/h")
]

AUX_NAME = [
    (0, _("Desinfection-1")),
    (1, _("Desinfection-2")),
    (2, _("Fountain-1")),
    (3, _("Fountain-2")),
    (4, _("Lighting-1")),
    (5, _("Lighting-2")),
    (6, _("Valve-1")),
    (7, _("Valve-2")),
    (8, _("GardenLighting-1")),
    (9, _("GardenLighting-2")),
    (10, _("Reverse Flow Machine")),
    (11, _("Domotica")),
    (12, _("Garden Fence")),
    (13, _("Window Blinds")),
    (14, _("None")),
    (15, _("Other"))
]

SEWER_CONFIG = [
    (0, _("No sewer valve")),
    (1, _("Manual sewer valve")),
    (2, _("Automatic sewer valve")),
]

VALVE_CONFIG = [
    (0, _("Manual")),
    (1, _("Pneumatic")),
    (2, _("Automatic"))
]

ECOVALVE_CONFIG = [
    (0, _("Off")),
    (1, _("Always on")),
    (2, _("Buffertank Regulation"))
]

# todo change to 70 days/weeks
# INTERVAL_PERIOD = [
#     (0, _("0 Weeks")),
#     (1, _("1 Week")),
#     (2, _("2 Weeks")),
#     (3, _("3 Weeks")),
#     (4, _("4 Weeks")),
#     (5, _("5 Weeks")),
#     (6, _("6 Weeks")),
#     (6, _("7 Weeks")),
# ]

WATER_LEVELS = [
    (0, _("Too low")),
    (1, _("Low")),
    (2, _("Ok")),
    (3, _("High")),
    (4, _("Too high")),
]

"""
min and max valudation at the form level (also in admin)
"""


class IntegerRangeField(models.IntegerField):

    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        validators = kwargs.pop('validators', [])
        validators.append(MinValueValidator(min_value)) if min_value else None
        validators.append(MaxValueValidator(max_value)) if max_value else None
        super().__init__(verbose_name=verbose_name, name=name, validators=validators, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class FloatRangeField(models.FloatField):

    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        validators = kwargs.pop('validators', [])
        validators.append(MinValueValidator(min_value)) if min_value else None
        validators.append(MaxValueValidator(max_value)) if max_value else None
        super().__init__(verbose_name=verbose_name, name=name, validators=validators, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class Account(AbstractUser):
    # inherited fields: username, password, first_name, last_name, email, is_staff, is_superuser, is_active, date_joined, last_login

    email = models.EmailField(blank=False, unique=True)
    tz = TimeZoneField(choices_display='WITH_GMT_OFFSET', default='Europe/Amsterdam', verbose_name="Timezone")

    groups = models.ManyToManyField(Group, related_name='account_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='account_permissions', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', ]

    def was_active_last_month(self):
        return self.last_login is not None and ( datetime.now(tz=timezone.utc) - self.last_login < timedelta(days=30) )

    def was_active_last_week(self):
        return self.last_login is not None and ( datetime.now(tz=timezone.utc) - self.last_login < timedelta(days=7) )

    def __str__(self):
        return self.email


class PoolBuilder(models.Model):
    objects = models.Manager()
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='poolbuilder', null=True)
    master = models.ForeignKey(Account, on_delete=models.DO_NOTHING, related_name='poolbuilders', null=True)

    street_name = models.CharField(verbose_name="Address", max_length=255, blank=True)
    city = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, blank=True)

    company_name = models.CharField(max_length=100, blank=True)
    company_phone = models.CharField(max_length=100, blank=True)

    # For Public api (one poolbuilder so far: Starline)
    api_key = models.CharField("API token", max_length=255, blank=True, db_index=True, help_text="PublicAPI access token, one per user")
    api_key_expiration = models.DateField("API token expiration date", blank=True, null=True, default=None)
    api_max_per_day = models.IntegerField("max API requests per day", blank=True, null=True, default=68400)  # 60 * 60 * 24h
    api_last_updated = models.DateField("Last updated", blank=True, null=True)
    api_count_today = models.IntegerField("todays API requests", blank=True, null=True)

    def generate_api_key(self):
        return ''.join(random.choice(string.ascii_uppercase) for _ in range(20))

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = "Poolbuilder"
        verbose_name_plural = "Poolbuilders"

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.svg', '.png', '.bmp', '.jpg', '.jpeg']
    if not ext in valid_extensions:
        raise ValidationError(u'File not supported!')


class PoolOwner(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='owner')
    objects = models.Manager()

    street_name = models.CharField(_("Street name"), max_length=255, blank=True)
    city = models.CharField(_("City"), max_length=30, blank=True)
    country = models.CharField(_("Country"), max_length=30, blank=True)

    latitude = models.FloatField(_("Latitude"), default=0.000000)   # Utrecht: 52.228936
    longitude = models.FloatField(_("Longitude"), default=0.000000) # Utrecht: 5.321492

    def __str__(self):
        return f"{self.account.first_name} {self.account.last_name}"



class Eps(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='eps')

    street_name = models.CharField(verbose_name="Address", blank=True, max_length=255)
    city = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, blank=True)

    company_name = models.CharField(max_length=100, blank=True)
    company_phone = models.CharField(max_length=100, blank=True)
    logo = models.ImageField('Logo', upload_to='eps/logos', null=True, blank=True)

    def __str__(self):
        return self.company_name

class PoolSetting(models.Model):
    """ master class they all link to
    Models with 1:1 with PoolSetting: Realtime, Configuration, Regulation, ControlPanel, Firmware, Notifications, NotificationWarnings, Status, Settings (+variants), Log, PoolSpecificupdates
    Poolsetting Links: history , realtimedata, guards , notifications , status,
    settings_general , settings_lighting , settings_timerpump , settings_aux1 , settings_aux2 , settings_aux3 , settings_aux4 , settings_temperaturesolar , settings_temperatureheating ,
    settings_ecovalve , settings_temperature , settings_backwash , settings_filterschedule1 , settings_filterschedule2 , settings_filterschedule3 , settings_rx , settings_ph , settings_filter ,
    settings_watersuppletion, settings_deck , settings_energytool
    logging, connect_event, pool_specific_update,
    configuration , regulation , controlpanel , firmware_version
    > guards: NotificationLimitModel
    > notifications: NotificationWarningModel
    """
    objects = models.Manager()
    poolname = models.CharField(_('Pool name'), max_length=30)
    poolnumber = models.CharField(_('Pool Number'), max_length=30, unique=True,
                                  help_text="Do not change unless PCB is changed")
    is_dirty = models.BooleanField(_('Dirty'), default=False,
                                   editable=False)  # Flag that it has been changed, will then be updated at target
    manual_mode = models.BooleanField(_('Manual mode'), default=False,
                                      editable=False)  # Handmatig bedienen van hardware, mag nooit true zjn, mag niet vanaf cloud

    poolbuilder = models.ForeignKey(PoolBuilder, on_delete=models.SET_NULL, null=True, related_name='pools')
    owner = models.ForeignKey(PoolOwner, on_delete=models.SET_NULL, null=True)

    # default bij Utrecht: 52   (EPS: 51.9057253)   (range: -90 90)
    latitude = models.FloatField(_("Latitude"), default=0.000000)

    # default bij Utrecht: 5    (EPS: 5.3352176)    (range: -180 180)
    longitude = models.FloatField(_("Longitude"), default=0.000000)

    # General settings
    version = models.CharField(_('Version'), max_length=5)
    logo = models.ImageField(_('Pool picture'), upload_to='pool/logos', blank=True, null=True,
                             help_text=" Maximum size 10MB")  # validators=[MaxSizeValidator(10000)

    class Meta:
        indexes = [
            models.Index(fields=['poolnumber']),
            models.Index(fields=['poolbuilder']),
            models.Index(fields=['owner'])
        ]

    def __str__(self):
        return str(self.poolnumber)


class HistoricalData(models.Model):
    """
    Stores current values with a timestamp, for making the charts
    # historicalData.objects.all()
    # historicalData.timescale.time_bucket()
    """
    poolsetting = models.ForeignKey(PoolSetting, on_delete=models.CASCADE, related_name="history", null=True)
    objects = models.Manager()

    water_temperature = models.FloatField((_('Water Temperature'), '°C'), default=20)
    ambient_temperature = models.FloatField((_('Ambient Temperature'), '°C'), default=20)
    solar_temperature = models.FloatField((_('Solar Temperature'), '°C'), default=20)
    filterpump_current = models.FloatField((_('Filterpump Power'), 'W'), default=1)

    ph = models.FloatField(('pH', ''), default=7)
    rx = models.FloatField(('Rx level', 'mV'), default=200)
    tds_ppm = models.FloatField(('TDS', 'ppm'), default=200)  # TDS sensor, meet conductivity (zout of pollution)
    clm_ppm = models.FloatField((_('Chlorine'), 'ppm'), default=600)

    time = models.DateTimeField('time')  # timezone aware timefield, inherited from TimescaleDB

    class Meta:
        verbose_name = "Historicaldata"
        verbose_name_plural = "Historicaldata"
        indexes = [
            models.Index(fields=["poolsetting"]),
            models.Index(fields=["time"]),
        ]

    def __str__(self):
        return str(self.poolsetting)


class RealTimeMeasurement(models.Model):
    """ Saves realtime measurements by date_time
    Acceptable min and max levels
        phL: 4 - 9
        clm: 0 - 3
        rx: 0 - 10000
        tds: 0 - 10000
        water: 0 - 40
        ambient: 0 - 60
        solar: 0 - 99
        level: 0 - 4
    """

    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name="realtimedata", null=True)
    objects = models.Manager()

    # General
    water_temperature = models.FloatField((_('Water Temperature'), '°C'), default=20)
    ambient_temperature = models.FloatField((_('Ambient Temperature'), '°C'), default=20)
    solar_temperature = models.FloatField((_('Solar Temperature'), '°C'), default=20)
    filterpump_current = models.FloatField((_('Filterpump current'), 'mA'), default=1)

    ph_actual = models.FloatField(('pH', ''), default=7)
    rx_actual = models.FloatField(('Rx level', 'mV'), default=200)

    # TDS sensor
    tds_ppm = models.IntegerField(('TDS', 'ppm'), default=200, help_text=_(
        "Raw value of the TDS sensor, measures conductivity (salt or pollution), not sent to cloud."))  # kan genegeerd worden; wordt verwijderd in nieuwere versies
    pollution_degree_ppm = models.IntegerField((_('Pollution'), 'ppm'), default=100,
                                               help_text=_("Measured by TDS sensor, same value as tds_ppm."))
    conductivity = models.FloatField((_('Conductivity'), 'S'), default=0.01, help_text=_(
        "salt/conductivity (measured by TDS sensor) = pollution degree ppm /  1.56."))

    clm_ppm = models.FloatField((_('Chlorine'), 'ppm'), default=0.00, help_text="Clm chlorine")
    empty_tank = models.BooleanField(_('Empty tank'), default=False)

    # Core temperature of IMX6
    imx_temperature = models.FloatField(_("IMX Temperature"), default=0.00)
    main_temperature = models.FloatField(_("Main temperature"), default=0.00)

    date_time = models.DateTimeField(default=now)
    error = models.IntegerField(default=0)

    def get_age(self):
        """
        # get_age < 180: online
        # get_age < 14400 (4u): warning
        # get_age > 4u: offline
        All data until now saved in UTC timezone
        Compare timezone aware datetimes, or not *both*
        {% if pool.realtimedata.get_age < 180 %}<i class="fas fa-circle text-success"></i>
        {% elif pool.realtimedata.get_age < 14400 %}<i class="fas fa-circle text-warning"></i>
        {% else %}<i class="fas fa-circle text-danger"></i>{% endif %}
        """
        return (datetime.now(tz=timezone.utc) - self.date_time).total_seconds()

    def date_time_nl(self):
        tz = pytz.timezone('Europe/Amsterdam')
        return self.date_time.astimezone(tz)

    def get_error(self):
        # True: ERROR IS GOED onder de 1000 en hoger dan 2000 -> success lampje
        # False: Als de embedded controller een error heeft, is deze gelegen tussen de 1000 en de 2000 -> error lampje
        return self.error < 1000 or self.error >= 2000

    def empty_tank_status(self):
        try:
            return self.poolsetting.status.empty  # 0=GOOD, 1=EMPTy
        except:
            return ''

    class Meta:
        verbose_name = "Real time measurement"
        verbose_name_plural = "Real time measurements"
        indexes = [
            models.Index(fields=["poolsetting"]),
            models.Index(fields=["date_time"]),
            models.Index(fields=["error"]),
        ]

    def __str__(self):
        return str(self.poolsetting)


class ConfigurationModel(models.Model):
    """ Unused, wordt niet gebruikt in huidige versie,
    wel werkend in nieuwe versie
    """

    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='configuration', null=True)
    is_dirty = models.BooleanField(_(' Dirty'), default=False,
                                   editable=False)  # Flag that it has been changed, will then be updated at target
    objects = models.Manager()

    PUMP_CHOICES = [
        (0, _('Pump Single Speed')),
        (1, 'Pentair SuperFlo'),
        (2, 'Pentair Intelliflo'),
        (3, 'Pump STL Inverter'),
        (4, 'Davey Promaster'),
        (5, 'Invertek Optidrive'),
        (6, 'Speck BADU Eco Touch Pro'),
        (7, 'Speck BADU 90 Eco Motion'),
        (8, 'Hayward Ecostar'),
        (9, 'Hayward VSTD'),
        (10, 'Zodiac Flo Pro VS'),
        (11, _('No Pump')),
    ]

    class BackwashChoices(models.IntegerChoices):
        SEMI_AUTO = 0, _('Semi-automatic')
        PNEU_VALVE = 1, _('Pneumatic valve')
        AUTO_VALVE = 2, _('Auto valve')

    volume_pool_m3 = models.IntegerField(_("Volume pool m3"), default=0)

    io_control_available = models.BooleanField(_("IO Control"), default=False)
    eh_control_available = models.BooleanField(_("EH control"), default=False)  # unused, use main_eh
    main_eh_control_available = models.BooleanField(_("TDS Salt"), default=False)  # betekent TDS salt meting
    tds_sensor_available = models.BooleanField(_("TDS Pollution"),
                                               default=False)  # betekent dat er een TDS pollution ingesteld is.
    water_level_sensor_available = models.BooleanField(_("Water Level Sensor"), default=False)
    clm_sensor_available = models.BooleanField(_("CLM Sensor"), default=False)
    external_off_available = models.BooleanField(_("External Off"), default=False)

    deck_available = models.BooleanField(_("Deck Enable"), default=False)  # 1. normale deck
    covco_deck_available = models.BooleanField(_("Covco Deck (NEXUS)"),
                                               default=False)  # 2. deck met cover control (nieuuw)
    remote_deck_control = models.BooleanField(_("Remote Deck Control"), default=False)  # to open|close|stop

    pump_type = models.IntegerField(_("Pump type"), default=0, choices=PUMP_CHOICES)
    backwash_valve_type = models.IntegerField(_("Backwash valve type"), default=0, choices=BackwashChoices.choices)
    sewer_config = models.IntegerField(_("Sewer config"), default=0,
                                       choices=SEWER_CONFIG)  # todo send and receive in API
    filterpump_stl = models.BooleanField(_("Filterpump STL"), default=False)
    watertemperature_protection = models.BooleanField(_("Watertemperature protection"), default=False)
    energytool_available = models.BooleanField(_("Energytool"), default=False)

    class Meta:
        indexes = [
            models.Index(fields=["poolsetting"]),
        ]
        verbose_name = "Configuration"
        verbose_name_plural = "Configurations"

    def save(self, *args, **kwargs):
        # if TDS measures salt, it doesn't measure pollution
        if self.main_eh_control_available:
            self.tds_sensor_available = False
        super(ConfigurationModel, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.poolsetting)


class RegulationModel(models.Model):
    """
    Not in use (probably)
    only used: lighting, temperature, cover (and probably in different model)
    was used only in api (setregulation called regularly, getregulation never)
    not used in new API
    """
    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='regulation', null=True)
    is_dirty = models.BooleanField(_('Dirty'), default=False,
                                   editable=False)  # Flag that it has been changed, will then be updated at target
    objects = models.Manager()

    lighting_regulation = models.BooleanField(_("Lighting regulation"), default=False)
    ph_regulation = models.BooleanField(_("pH"), default=False)
    rx_regulation = models.BooleanField(_("Rx"), default=False)
    electrolyse_regulation = models.BooleanField(_("Electrolyse regulation"), default=False)
    flake_regulation = models.BooleanField(_("Flake regulation"), default=False)
    timer_regulation = models.BooleanField(_("Timer regulation"), default=False)
    shock_regulation = models.BooleanField(_("Shock regulation"), default=False)
    tds_regulation = models.BooleanField(_("RDS regulation"), default=False)
    temperature_regulation = models.BooleanField(_("Temperature regulation"), default=False)
    cover_regulation = models.BooleanField(_("Cover regulation"), default=False)


class ControlPanelModel(models.Model):
    """ unused (was for manual control)
    unused in code: CommandView, CommandReceiverSerializer
    """
    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='controlpanel', null=True)
    is_dirty = models.BooleanField(_('Dirty'), default=False,
                                   editable=False)  # Flag that it has been changed, will then be updated at target
    objects = models.Manager()

    aux1 = models.BooleanField(default=False)
    aux2 = models.BooleanField(default=False)
    aux3 = models.BooleanField(default=False)
    aux4 = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=["poolsetting"]), ]
        verbose_name = "ControlPanel"
        verbose_name_plural = "ControlPanel"


class FirmwareVersionModel(models.Model):
    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='firmware_version',
                                       null=True)
    objects = models.Manager()

    version_gui = models.CharField(_("Version GUI"), max_length=6, default="")
    version_main = models.CharField(_("Version Main"), max_length=6, default="")
    version_io = models.CharField(_("Versoin IO"), max_length=6, default="")
    version_eh = models.CharField(_("Version EH"), max_length=6, default="")
    version_wl = models.CharField(_("Version WL"), max_length=6, default="")
    version_deck = models.CharField(_("Version Deck"), max_length=6, default="")
    last_updated = models.DateTimeField(_("Last updated"), default=now)

    def __str__(self):
        return str(self.poolsetting)


class SerialNumberWhiteList(models.Model):  # unused
    serialnumber = models.CharField(_("Serial Number"), max_length=30)


class CommandSender(models.Model):  # unused
    serialnumber = models.CharField(_("Serial Number"), max_length=30)


class NotificationLimitModel(models.Model):
    """
    Acceptable min and max levels
        ph: 4 - 9
        clm: 0 - 3
        rx: 0 - 10000
        tds: 0 - 10000
        water temperature: 0 - 40
        ambient temperature: 0 - 60
        solar temperature: 0 - 99
        water level: 0 - 4
    Sends optional email notification if outside boundary
    Time elapsed is the last updated date
    """
    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='guards', null=True)
    objects = models.Manager()

    ph_notification_measurement = models.BooleanField(_("pH measurement notification"), default=False)
    ph_min_limit = FloatRangeField(_("pH minimum value"), default=4.0, min_value=4, max_value=9)
    ph_max_limit = FloatRangeField(_("pH maximum value"), default=9.0, min_value=4.1, max_value=9)
    ph_notification_time = models.TimeField(_("pH delay time for email"), default=datetime.utcfromtimestamp(0))
    ph_notification_time_elapsed = models.DateTimeField(_("pH Notification Time elapsed"),
                                                        default=datetime.fromtimestamp(3600,
                                                                                       tz=timezone.utc))  # 1jan 1970 01:00
    ph_mail_time_elapsed = models.DateTimeField(_("pH Mail Time elapsed"),
                                                default=datetime.fromtimestamp(3600, tz=timezone.utc))

    rx_notification_measurement = models.BooleanField(_("Rx measurement notification"), default=False)
    rx_min_limit = FloatRangeField(_("Rx minimum value (mV)"), default=0, min_value=0, max_value=10000)
    rx_max_limit = FloatRangeField(_("Rx maximum value (mV)"), default=800, min_value=1, max_value=10000)
    rx_notification_time = models.TimeField(_("Rx delay time for email"), default=datetime.utcfromtimestamp(0))
    rx_notification_time_elapsed = models.DateTimeField(_("RX Notification Time elapsed"),
                                                        default=datetime.fromtimestamp(3600, tz=timezone.utc))
    rx_mail_time_elapsed = models.DateTimeField(_("RX Mail Time elapsed"),
                                                default=datetime.fromtimestamp(3600, tz=timezone.utc))

    clm_notification_measurement = models.BooleanField(_("CLM measurement notification"), default=False)
    clm_min_limit = FloatRangeField(_("CLM minimum value (ppm)"), default=0, min_value=0, max_value=3)
    clm_max_limit = FloatRangeField(_("CLM maximum value (ppm)"), default=0, min_value=0, max_value=3)
    clm_notification_time = models.TimeField(_("Clm delay time for email"), default=datetime.utcfromtimestamp(0))
    clm_notification_time_elapsed = models.DateTimeField(_("CLM Notification Time elapsed"),
                                                         default=datetime.fromtimestamp(3600, tz=timezone.utc))
    clm_mail_time_elapsed = models.DateTimeField(_("CLM Mail Time Elapsed"),
                                                 default=datetime.fromtimestamp(3600, tz=timezone.utc))

    water_notification_measurement = models.BooleanField(_("Water temperature measurement notification"), default=False)
    water_min_limit = FloatRangeField(_("Water Temperature minimum (°C)"), default=0, min_value=0, max_value=40)
    water_max_limit = FloatRangeField(_("Water Temperature maximum (°C)"), default=10, min_value=1, max_value=40)
    water_notification_time = models.TimeField(_("Water Temperature delay time for email"),
                                               default=datetime.utcfromtimestamp(0))
    water_notification_time_elapsed = models.DateTimeField(_("Water Temperature Notification time elapsed"),
                                                           default=datetime.fromtimestamp(3600, tz=timezone.utc))
    water_mail_time_elapsed = models.DateTimeField(_("Water temperature maximum (°C)"),
                                                   default=datetime.fromtimestamp(3600, tz=timezone.utc))

    ambient_notification_measurement = models.BooleanField(_("Ambient measurement notification"), default=False)
    ambient_min_limit = FloatRangeField(_("Ambient temperature minimum (°C)"), default=0, min_value=0, max_value=60)
    ambient_max_limit = FloatRangeField(_("Ambient temperature maximum (°C)"), default=10, min_value=1, max_value=60)
    ambient_notification_time = models.TimeField(_("Ambient temperature delay time for email"),
                                                 default=datetime.utcfromtimestamp(0))
    ambient_notification_time_elapsed = models.DateTimeField(_("Ambient temperature notification time elapsed"),
                                                             default=datetime.fromtimestamp(3600, tz=timezone.utc))
    ambient_mail_time_elapsed = models.DateTimeField(_("Ambient temperature email time elapsed"),
                                                     default=datetime.fromtimestamp(3600, tz=timezone.utc))

    solar_notification_measurement = models.BooleanField(_("Solar measurement notification"), default=False)
    solar_min_limit = FloatRangeField(_("Solar temperature minimum (°C)"), default=0, min_value=0, max_value=99)
    solar_max_limit = FloatRangeField(_("Solar temperature maximum (°C)"), default=10, min_value=1, max_value=99)
    solar_notification_time = models.TimeField(_("Solar temperature delay time for email"),
                                               default=datetime.utcfromtimestamp(0))
    solar_notification_time_elapsed = models.DateTimeField(_("Solar notification time elapsed"),
                                                           default=datetime.fromtimestamp(3600, tz=timezone.utc))
    solar_mail_time_elapsed = models.DateTimeField(_("Solar mail time elapsed"),
                                                   default=datetime.fromtimestamp(3600, tz=timezone.utc))

    level_notification_measurement = models.BooleanField(_("Level measurement notification"), default=False)
    level_min_limit = models.IntegerField(default=0, choices=WATER_LEVELS)
    level_max_limit = models.IntegerField(default=4, choices=WATER_LEVELS)
    level_notification_time = models.TimeField("Level delay time for email (min)", default=datetime.utcfromtimestamp(0))
    level_notification_time_elapsed = models.DateTimeField(default=datetime.fromtimestamp(3600, tz=timezone.utc))
    level_mail_time_elapsed = models.DateTimeField(default=datetime.fromtimestamp(3600, tz=timezone.utc))

    tds_notification_measurement = models.BooleanField(_("TDS measurement notification"), default=False,
                                                       help_text=_("Conductivity (salt or pollution)"))
    tds_min_limit = IntegerRangeField(_("Tds minimum limit"), default=0, min_value=0, max_value=10000)
    tds_max_limit = IntegerRangeField(_("Tds maximum limit"), default=10, min_value=1, max_value=10000)
    tds_notification_time = models.TimeField(_("TDS delay time for email"), default=datetime.utcfromtimestamp(0))
    tds_notification_time_elapsed = models.DateTimeField(_("TDS Notification Time Elapsed"),
                                                         default=datetime.fromtimestamp(3600, tz=timezone.utc))
    tds_mail_time_elapsed = models.DateTimeField(_("TDS Email Time Elapsed"),
                                                 default=datetime.fromtimestamp(3600, tz=timezone.utc))

    empty_notification_measurement = models.BooleanField(_("Empty tank notification"), default=False)
    empty_notification_time = models.TimeField(_("Empty tank delay time for email"),
                                               default=datetime.utcfromtimestamp(0))
    empty_notification_time_elapsed = models.DateTimeField(_("Empty tank notification time elapsed"),
                                                           default=datetime.fromtimestamp(3600, tz=timezone.utc))
    empty_mail_time_elapsed = models.DateTimeField(_("Empty tank mail time elapsed"),
                                                   default=datetime.fromtimestamp(3600, tz=timezone.utc))

    email1 = models.EmailField(default='', verbose_name=_("Your emailaddress for notifications"), blank=True)
    email2 = models.EmailField(default='', verbose_name=_("Second email for notifications"), blank=True)
    email3 = models.EmailField(default='', verbose_name=_("Third email for notifications"), blank=True)
    email4 = models.EmailField(default='', verbose_name=_("Fourth email for notifications"), blank=True)
    email5 = models.EmailField(default='', verbose_name=_("Fifth email for notifications"), blank=True)

    def has_email(self):
        return self.email1 or self.email2 or self.email3 or self.email4 or self.email5

    def save(self, *args, **kwargs):
        """  Does checks on min and max values  (TODO clean up bad values)
        This ensures full_clean is called to perform model validation (min, max, max_length)
        Causes errors like level_max_limit': ['Value 10 is not a valid choice.']
        """
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        indexes = [models.Index(fields=["poolsetting"]), ]
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return str(self.poolsetting)


class NotificationWarnings(models.Model):
    """
    Has current status
    Only api.views updates, has the logic for when is good/fault
    example: ph=NotificationWarnings.PoolStatus.GOOD
    """

    class PoolStatus(models.IntegerChoices):
        GOOD = 0
        FAULT = 1

    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='notifications', null=True)
    objects = models.Manager()

    ph = models.IntegerField(_("pH status"), choices=PoolStatus.choices, default=0)
    rx = models.IntegerField(_("Rx status"), choices=PoolStatus.choices, default=0)
    clm = models.IntegerField(_("CLM status"), choices=PoolStatus.choices, default=0)
    t_water = models.IntegerField(_("Water temperature status"), choices=PoolStatus.choices,
                                  default=0)  # water temperature
    t_ambient = models.IntegerField(_("Ambient tempeature status"), choices=PoolStatus.choices,
                                    default=0)  # ambient temperature
    t_solar = models.IntegerField(_("Solar temperature status"), choices=PoolStatus.choices,
                                  default=0)  # solar temperature
    level = models.IntegerField(_("Water level status"), choices=PoolStatus.choices, default=0)  # water level
    tds = models.IntegerField(_("TDS status"), choices=PoolStatus.choices, default=0)
    empty = models.IntegerField(_("Empty tank status"), choices=PoolStatus.choices, default=0)  # empty tank

    def __str__(self):
        return str(self.poolsetting)


class StatusModel(models.Model):
    """ Info saved by api, used in controls (waterheight) but not much else """

    class PoolStatus(models.IntegerChoices):
        GOOD = 0
        FAULT = 1

    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='status', null=True)
    objects = models.Manager()

    cover = models.IntegerField(_("Cover status"), default=0)
    cover_error = models.IntegerField(_("Cover error"), default=0)
    filter = models.IntegerField(_("Water Filter status"), default=0)
    temperature = models.IntegerField(_("Temperature status"), default=0)
    lighting = models.IntegerField(_("Lighting status"), default=0)
    waterheight = models.IntegerField(_("Waterheight status"), default=0)
    aux1 = models.IntegerField(_("Aux1 status"), null=True, default=0)
    aux2 = models.IntegerField(_("Aux2 status"), null=True, default=0)
    aux3 = models.IntegerField(_("Aux3 status"), null=True, default=0)
    aux4 = models.IntegerField(_("Aux4 status"), null=True, default=0)

    ph = models.IntegerField(_("pH"), default=0)  # ph_error
    rx = models.IntegerField(_("Rx"), default=0)  # rx_error
    clm = models.IntegerField(_("CLM status"), choices=PoolStatus.choices, default=0)
    t_water = models.IntegerField(_("Water temperature status"), choices=PoolStatus.choices,
                                  default=0)  # water temperature
    t_ambient = models.IntegerField(_("Ambient tempeature status"), choices=PoolStatus.choices,
                                    default=0)  # ambient temperature
    t_solar = models.IntegerField(_("Solar temperature status"), choices=PoolStatus.choices,
                                  default=0)  # solar temperature
    level = models.IntegerField(_("Water level status"), choices=PoolStatus.choices, default=0)  # water level
    tds = models.IntegerField(_("TDS status"), choices=PoolStatus.choices, default=0)
    empty = models.IntegerField(_("Empty tank status"), choices=PoolStatus.choices, default=0)  # empty tank

    pump = models.IntegerField(_("Pump status"), default=0)
    pumpspeed = models.IntegerField(_("Pumpspeed status"), default=0)
    backwash = models.IntegerField(_("Backwash status"), default=0)
    flow = models.IntegerField(_("Flow status"), default=0)

    datetime = models.DateTimeField(_("datetime"), default=now)

    class Meta:
        verbose_name = "Status model"
        verbose_name_plural = "Status model"

    def __str__(self):
        return str(self.poolsetting)


class StatusPump(models.Model):  # pump also in StatusModel
    objects = models.Manager()
    poolsetting = models.ForeignKey(PoolSetting, on_delete=models.CASCADE, related_name="pump", null=True)
    pump = models.IntegerField(_("Pump status"), default=0)
    datetime = models.DateTimeField(db_index=True)


class StatusFlow(models.Model):  # flow also in StatusModel
    objects = models.Manager()
    poolsetting = models.ForeignKey(PoolSetting, on_delete=models.CASCADE, related_name="flow", null=True)
    flow = models.IntegerField(_("Flow"), default=0)
    datetime = models.DateTimeField(db_index=True)


class StatusBackwash(models.Model):  # backwash also in StatusModel
    objects = models.Manager()
    poolsetting = models.ForeignKey(PoolSetting, on_delete=models.CASCADE, related_name="backwash", null=True)
    backwash = models.IntegerField(_("Backwash"), default=0)
    datetime = models.DateTimeField(db_index=True)

    class Meta:
        verbose_name = "Status backwash"
        verbose_name_plural = "Status backwash"


class SettingsGeneralModel(models.Model):
    # /pools/settings/pk/general
    # shown, not used by api
    objects = models.Manager()
    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='settings_general',
                                       null=True)
    formname = 'SettingsGeneralForm'

    general_pause = models.BooleanField(_("General pause"), default=False)
    general_flow_alarm = models.BooleanField(_("General flow alarm"), default=False)
    general_offcontact = models.IntegerField(_("General Off Contact Regulation"), default=0, choices=EXTOFF_CHOICES)
    general_alarm = models.IntegerField(_("General alarm"), choices=ALARM_CHOICES, default=0)
    general_ph_rx_pump_volume = models.IntegerField(_("pH Rx Pump volume"), default=0, choices=PUMP_VOLUME)
    general_boot_delay = IntegerRangeField(_("Boot delay (s)"), default=0, min_value=0, max_value=999)
    general_standby_time = IntegerRangeField(_("Standy time (s)"), default=0, min_value=0, max_value=999)
    general_language = models.IntegerField(_("General language"), default=0, choices=LANGUAGES)

    def save(self, *args, **kwargs):
        self.full_clean()  # This ensures model validation is done (min_value, max_value, max_length)
        super().save(*args, **kwargs)

    @property
    def preferred_language(self):
        try:
            return LANGUAGES[self.general_language][1]
        except:
            return "Nederlands"

    @property
    def preferred_language_code(self):
        try:
            return LANGUAGES_CODE[self.general_language][1]
        except:
            return "nl"

    class Meta:
        indexes = [models.Index(fields=["poolsetting"]), ]
        verbose_name = "Settings General"
        verbose_name_plural = "Settings General"


class SettingsLightingModel(models.Model):
    objects = models.Manager()
    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='settings_lighting',
                                       null=True)
    depends_on = 'io_control_available'
    formname = 'SettingsLightingForm'

    LIGHT_CONFIGURATION = [
        (0, _("Single Colour")),
        (1, _("Rotating RGB")),
        (2, _("STL-RGB"))
    ]
    LIGHT_COLOUR = [
        (0, "White"),
        (1, "Red"),
        (2, "Blue"),
        (3, "Green"),
        (4, "Magenta"),
        (5, "Cyan"),
        (6, "Yellow"),
        (7, "Seq1"),
        (8, "Seq2"),
        (9, "Seq3"),
        (10, "Seq4"),
        (11, "Seq5"),
        (12, "Disco1"),
        (13, "Disco2")
    ]

    lighting_regulation = models.BooleanField(_("Lighting regulation"), default=False)
    lighting_active = models.BooleanField(_("Lighting active"), default=False)
    lighting_schedule = models.BooleanField(_("Lighting schedule"), default=False)  # saved but unused

    lighting_start_time = models.TimeField(_("Lighting start time"), default=datetime.utcfromtimestamp(0))
    lighting_stop_time = models.TimeField(_("Lighting stop time"), default=datetime.utcfromtimestamp(0))
    lighting_monday = models.BooleanField(_("Lighting monday"), default=False)
    lighting_tuesday = models.BooleanField(_("Lighting tuesday"), default=False)
    lighting_wednesday = models.BooleanField(_("Lighting wednesday"), default=False)
    lighting_thursday = models.BooleanField(_("Lighting thursday"), default=False)
    lighting_friday = models.BooleanField(_("LIghting friday"), default=False)
    lighting_saturday = models.BooleanField(_("Lighting saturday"), default=False)
    lighting_sunday = models.BooleanField(_("Lighting sunday"), default=False)

    lighting_on_deck_closed = models.BooleanField(_("Switch off when cover is closed"), default=False)
    lighting_configuration = models.IntegerField(_("Lighting configuration"), default=0, choices=LIGHT_CONFIGURATION)
    lighting_colour_stl = models.IntegerField(_("LIghting colour STI"), default=0, choices=LIGHT_COLOUR)
    lighting_rgb_stl_time = IntegerRangeField(_("STL Rotating RGB Pulse time"), default=150, min_value=0, max_value=999)
    lighting_next_colour = models.BooleanField(_("Lighting next colour"), default=False)

    @property
    def active_days(self):
        if not self.lighting_regulation or not self.lighting_active:
            return None
        days = []
        days.append('Mon') if self.lighting_monday else None
        days.append('Tue') if self.lighting_tuesday else None
        days.append('Wed') if self.lighting_wednesday else None
        days.append('Thu') if self.lighting_thursday else None
        days.append('Fri') if self.lighting_friday else None
        days.append('Sat') if self.lighting_saturday else None
        days.append('Sun') if self.lighting_sunday else None
        return ', '.join(days)

    def save(self, *args, **kwargs):
        self.full_clean()  # This ensures model validation is done (min_value, max_value, max_length)
        super().save(*args, **kwargs)


class SettingsTimerPumpsModel(models.Model):  # form shown, not further used

    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='settings_timerpumps',
                                       null=True)
    formname = 'SettingsTimerPumpsForm'
    objects = models.Manager()

    timerpumps_timer1_wait_time = IntegerRangeField(_("Timer 1 wait time (h)"), default=0, min_value=0, max_value=999)
    timerpumps_timer1_dosing_time = IntegerRangeField(_("Timer 1 dosing time (min)"), default=0, min_value=0,
                                                      max_value=999)
    timerpumps_timer2_wait_time = IntegerRangeField(_("Timer 2 wait time (h)"), default=0, min_value=0, max_value=999)
    timerpumps_timer2_dosing_time = IntegerRangeField(_("Timer 2 dosing time (min)"), default=0, min_value=0,
                                                      max_value=999)

    def save(self, *args, **kwargs):
        self.full_clean()  # This ensures model validation is done (min_value, max_value, max_length)
        super().save(*args, **kwargs)


class SettingsAux1Model(models.Model):
    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='settings_aux1', null=True)
    depends_on = 'io_control_available'
    formname = 'SettingsAux1Form'
    objects = models.Manager()

    aux1_regulation = models.BooleanField(_("Aux 1 regulation"), default=False)
    aux1_activate = models.BooleanField(_("Aux 1 activate"), default=False)
    aux1_name = models.IntegerField(_("Aux 1 name "), default=0, choices=AUX_NAME)
    aux1_flow = models.BooleanField(_("Aux 1 flow control"), default=False)
    aux1_on_deck_closed = models.BooleanField(_("Switch off when cover is closed"), default=False)

    aux1_schedule = models.BooleanField(_("Aux 1 schedule"), default=False)
    aux1_start_time = models.TimeField(_("Aux 1 start time"), default=datetime.utcfromtimestamp(0))
    aux1_stop_time = models.TimeField(_("Aux 1 stop time"), default=datetime.utcfromtimestamp(0))
    aux1_monday = models.BooleanField(_("Aux 1 Monday"), default=False)
    aux1_tuesday = models.BooleanField(_("Aux 1 Tuesday"), default=False)
    aux1_wednesday = models.BooleanField(_("Aux 1 Wednesday"), default=False)
    aux1_thursday = models.BooleanField(_("Aux 1 Thursday"), default=False)
    aux1_friday = models.BooleanField(_("Aux 1 Friday"), default=False)
    aux1_saturday = models.BooleanField(_("Aux 1 Saturday"), default=False)
    aux1_sunday = models.BooleanField(_("Aux 1 Sunday"), default=False)


class SettingsAux2Model(models.Model):
    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='settings_aux2', null=True)
    depends_on = 'io_control_available'
    formname = 'SettingsAux2Form'
    objects = models.Manager()

    aux2_regulation = models.BooleanField(_("Aux 2 regulation"), default=False)
    aux2_activate = models.BooleanField(_("Aux 2 activate"), default=False)
    aux2_name = models.IntegerField(_("Aux 2 name"), default=0, choices=AUX_NAME)
    aux2_flow = models.BooleanField(_("Aux 2 flow control"), default=False)
    aux2_on_deck_closed = models.BooleanField(_("Switch off when cover is closed"), default=False)

    aux2_schedule = models.BooleanField(_("Aux 2 schedule"), default=False)
    aux2_start_time = models.TimeField(_("Aux 2 start time"), default=datetime.utcfromtimestamp(0))
    aux2_stop_time = models.TimeField(_("Aux 2 stop time"), default=datetime.utcfromtimestamp(0))
    aux2_monday = models.BooleanField(_("Aux 2 monday"), default=False)
    aux2_tuesday = models.BooleanField(_("Aux 2 tuesday"), default=False)
    aux2_wednesday = models.BooleanField(_("Aux 2 wednesdy"), default=False)
    aux2_thursday = models.BooleanField(_("Aux 2 thursday"), default=False)
    aux2_friday = models.BooleanField(_("Aux 2 friday"), default=False)
    aux2_saturday = models.BooleanField(_("Aux 2 saturday"), default=False)
    aux2_sunday = models.BooleanField(_("Aux 2 sunday"), default=False)


class SettingsAux3Model(models.Model):
    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='settings_aux3', null=True)
    depends_on = 'io_control_available'
    formname = 'SettingsAux3Form'
    objects = models.Manager()

    aux3_regulation = models.BooleanField(_("Aux 3 regulation"), default=False)
    aux3_activate = models.BooleanField(_("Aux 3 activate"), default=False)
    aux3_flow = models.BooleanField(_("Aux 3 Flow Control"), default=False)
    aux3_name = models.IntegerField(_("Aux 3 name"), default=0, choices=AUX_NAME)
    aux3_on_deck_closed = models.BooleanField(_("Switch off when cover is closed"), default=False)

    aux3_schedule = models.BooleanField(_("Aux 3 schedule"), default=False)
    aux3_start_time = models.TimeField(_("Aux 3 start time"), default=datetime.utcfromtimestamp(0))
    aux3_stop_time = models.TimeField(_("Aux 3 stop time"), default=datetime.utcfromtimestamp(0))
    aux3_monday = models.BooleanField(_("Aux 3 monday"), default=False)
    aux3_tuesday = models.BooleanField(_("Aux 3 tuesday"), default=False)
    aux3_wednesday = models.BooleanField(_("Aux 3 wednesday "), default=False)
    aux3_thursday = models.BooleanField(_("Aux 3 thursday"), default=False)
    aux3_friday = models.BooleanField(_("Aux 3 friday"), default=False)
    aux3_saturday = models.BooleanField(_("Aux 3 saturday"), default=False)
    aux3_sunday = models.BooleanField(_("Aux 3 sunday"), default=False)


class SettingsAux4Model(models.Model):
    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='settings_aux4', null=True)
    depends_on = 'io_control_available'
    formname = 'SettingsAux4Form'
    objects = models.Manager()

    aux4_regulation = models.BooleanField(_("Aux 4 regulation"), default=False)
    aux4_activate = models.BooleanField(_("Aux 4 activate"), default=False)
    aux4_flow = models.BooleanField(_("Aux 4 Flow Control"), default=False)
    aux4_schedule = models.BooleanField(_("Aux 4 schedule"), default=False)
    aux4_start_time = models.TimeField(_("Aux 4 start time"), default=datetime.utcfromtimestamp(0))
    aux4_stop_time = models.TimeField(_("Aux 4 stop time"), default=datetime.utcfromtimestamp(0))
    aux4_monday = models.BooleanField(_("Aux 4 monday"), default=False)
    aux4_tuesday = models.BooleanField(_("Aux 3 tuesday"), default=False)
    aux4_wednesday = models.BooleanField(_("Aux 4 wednesday"), default=False)
    aux4_thursday = models.BooleanField(_("Aux 4 thursday"), default=False)
    aux4_friday = models.BooleanField(_("Aux 4 friday"), default=False)
    aux4_saturday = models.BooleanField(_("Aux 4 saturday"), default=False)
    aux4_sunday = models.BooleanField(_("Aux 4 sunday"), default=False)
    aux4_name = models.IntegerField(_("Aux 4 name"), default=0, choices=AUX_NAME)
    aux4_on_deck_closed = models.BooleanField(_("Switch off when cover is closed"), default=False)


class SettingsTemperatureSolarModel(models.Model):
    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='settings_temperaturesolar',
                                       null=True)
    depends_on = 'io_control_available'
    formname = 'SettingsTemperatureSolarForm'
    objects = models.Manager()

    temperaturesolar_regulation = models.BooleanField(_("Solar Temperature regulation"), default=False, editable=False)
    temperaturesolar_temperature_offset = FloatRangeField(_("Solar Temperature offset"), default=0.0, min_value=0,
                                                          max_value=999, editable=False)
    temperaturesolar_pump_speed = IntegerRangeField(_("Solar Temperature pump speed"), default=0, min_value=0,
                                                    max_value=4, editable=False)
    temperaturesolar_sp_too_high = FloatRangeField(_("Solar Temperature SP too high "), default=0.0, min_value=0,
                                                   max_value=999, editable=False)
    temperaturesolar_sp_high = FloatRangeField(_("Solar temperature SP high"), default=0.0, min_value=0, max_value=999,
                                               editable=False)

    def pump_speed_str(self):
        try:
            return PUMP_SPEEDS[self.temperaturesolar_pump_speed][1]
        except:
            return ''

    def save(self, *args, **kwargs):
        self.full_clean()  # This ensures model validation is done (min_value, max_value, max_length)
        super().save(*args, **kwargs)


class SettingsTemperatureHeatingModel(models.Model):
    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE,
                                       related_name='settings_temperatureheating', null=True)
    depends_on = 'io_control_available'
    formname = 'SettingsTemperatureHeatingForm'
    objects = models.Manager()

    temperatureheating_regulation = models.BooleanField(_("Heating regulation"), default=False)
    temperatureheating_interval = IntegerRangeField(_("Heating interval (min)"), default=0, min_value=0, max_value=999)
    temperatureheating_priority = models.BooleanField(_("Heating priority"), default=False)
    temperatureheating_cooling_period = IntegerRangeField(_("Heating cooling period (s)"), default=0, min_value=0,
                                                          max_value=999)
    temperatureheating_pump_speed = models.IntegerField(_("Heating pump speed"), default=0, choices=PUMP_SPEEDS)
    temperature_frost_protection = models.BooleanField(_("Temperature frost protection"), default=False)  # moved

    def pump_speed_str(self):
        try:
            return PUMP_SPEEDS[self.temperatureheating_pump_speed][1]
        except:
            return ''

    def save(self, *args, **kwargs):
        self.full_clean()  # This ensures model validation is done (min_value, max_value, max_length)
        super().save(*args, **kwargs)


class SettingsTemperatureModel(models.Model):
    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='settings_temperature',
                                       null=True)
    depends_on = 'io_control_available'
    formname = 'SettingsTemperatureForm'
    objects = models.Manager()

    temperature_water_target = FloatRangeField(_("Water temperature desired (°C)"), default=0.0, min_value=0.0,
                                               max_value=32.0, null=True)
    temperature_frost_protection = models.BooleanField(_("Temperature frost protection (old)"),
                                                       default=False)  # old one 2023

    def save(self, *args, **kwargs):
        # {'temperature_water_target': ['Ensure this value is less than or equal to 32.0.']}
        self.full_clean()  # This ensures model validation is done (min_value, max_value, max_length)
        super().save(*args, **kwargs)


class SettingsEcoValveModel(models.Model):
    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='settings_ecovalve',
                                       null=True)
    depends_on = 'io_control_available'
    formname = 'SettingsEcoValveForm'
    objects = models.Manager()

    filterecovalve_always_active = models.BooleanField(_("Filter ecovalve always active"), default=False)
    filterecovalve_buffertank = models.BooleanField(_("Filter ecovalve buffertank"), default=False)
    filterecovalve_mode = models.IntegerField(_("Filter ecovalve mode"), default=0, choices=ECOVALVE_CONFIG)

    def save(self, *args, **kwargs):
        self.full_clean()  # This ensures model validation is done (min_value, max_value, max_length)
        super().save(*args, **kwargs)


class SettingsBackwashModel(models.Model):
    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='settings_backwash',
                                       null=True)
    depends_on = 'io_control_available'
    formname = 'SettingsBackwashForm'
    objects = models.Manager()

    filterbackwash_regulation = models.BooleanField(_("Filter backwash regulation"), default=False)
    filterbackwash_interval_period = models.PositiveIntegerField(_("Filter backwash interval period"), default=0,
                                                                 help_text="In days or weeks")  # extend to 0-70 (days/weeks),choices=INTERVAL_PERIOD
    filterbackwash_pump_speed = models.IntegerField(_("Filter backwash pump speed"), default=0, choices=PUMP_SPEEDS)
    filterbackwash_backwash_duration = IntegerRangeField(_("Backwash duration (s)"), default=0, min_value=0,
                                                         max_value=999)
    filterbackwash_rinse_duration = IntegerRangeField(_("Rinse duration (s)"), default=0, min_value=0, max_value=999)
    filterbackwash_config_rinse = models.BooleanField(_("Filter backwash config rinse"), default=False)
    filterbackwash_start = models.BooleanField(_("Filter backwash start"), default=False)

    def pump_speed_str(self):
        try:
            return PUMP_SPEEDS[self.filterbackwash_pump_speed][1]
        except:
            return ''

    def save(self, *args, **kwargs):
        self.full_clean()  # This ensures model validation is done (min_value, max_value, max_length)
        super().save(*args, **kwargs)


class SettingsFilterSchedule1Model(models.Model):
    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='settings_filterschedule1',
                                       null=True)
    depends_on = 'io_control_available'
    formname = 'SettingsFilterSchedule1Form'
    objects = models.Manager()

    filterschedule1_enabled = models.BooleanField(_("Filter schedule 1 enabled"), default=False)
    filterschedule1_start_time = models.TimeField(_("Filter schedule 1 start time"),
                                                  default=datetime.utcfromtimestamp(0))
    filterschedule1_stop_time = models.TimeField(_("Filter schedule 1 stop time"), default=datetime.utcfromtimestamp(0))
    filterschedule1_monday = models.BooleanField(_("Filter schedule 1 monday"), default=False)
    filterschedule1_tuesday = models.BooleanField(_("Filter schedule 1 tuesday"), default=False)
    filterschedule1_wednesday = models.BooleanField(_("Filter schedule 1 wednesday"), default=False)
    filterschedule1_thursday = models.BooleanField(_("Filter schedule 1 thursday"), default=False)
    filterschedule1_friday = models.BooleanField(_("Filter schedule 1 friday"), default=False)
    filterschedule1_saturday = models.BooleanField(_("Filter schedule 1 saturday"), default=False)
    filterschedule1_sunday = models.BooleanField(_("Filter schedule 1 sunday"), default=False)
    filterschedule1_pump_speed = models.IntegerField(_("Filter schedule 1 pump speed"), default=0, choices=PUMP_SPEEDS)

    @property
    def active_days(self):
        if not self.filterschedule1_enabled:
            return None
        days = []
        days.append('Mon') if self.filterschedule1_monday else None
        days.append('Tue') if self.filterschedule1_tuesday else None
        days.append('Wed') if self.filterschedule1_wednesday else None
        days.append('Thu') if self.filterschedule1_thursday else None
        days.append('Fri') if self.filterschedule1_friday else None
        days.append('Sat') if self.filterschedule1_saturday else None
        days.append('Sun') if self.filterschedule1_sunday else None
        return ', '.join(days)

    @property
    def pump_speed_str(self):
        try:
            return PUMP_SPEEDS[self.filterschedule1_pump_speed][1]
        except:
            return ''


class SettingsFilterSchedule2Model(models.Model):
    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='settings_filterschedule2',
                                       null=True)
    depends_on = 'io_control_available'
    formname = 'SettingsFilterSchedule2Form'
    objects = models.Manager()

    filterschedule2_enabled = models.BooleanField(_("Filter schedule 2 enabled"), default=False)
    filterschedule2_start_time = models.TimeField(_("Filter schedule 2 start time"),
                                                  default=datetime.utcfromtimestamp(0))
    filterschedule2_stop_time = models.TimeField(_("Filter schedule 2 stop time"), default=datetime.utcfromtimestamp(0))
    filterschedule2_monday = models.BooleanField(_("Filter schedule 2 monday"), default=False)
    filterschedule2_tuesday = models.BooleanField(_("Filter schedule 2 tuesday"), default=False)
    filterschedule2_wednesday = models.BooleanField(_("Filter schedule 2 wednesday"), default=False)
    filterschedule2_thursday = models.BooleanField(_("Filter schedule 2 thursday"), default=False)
    filterschedule2_friday = models.BooleanField(_("Filter schedule 2 friday"), default=False)
    filterschedule2_saturday = models.BooleanField(_("Filter schedule 2 saturday"), default=False)
    filterschedule2_sunday = models.BooleanField(_("Filter schedule 2 sunday"), default=False)
    filterschedule2_pump_speed = models.IntegerField(_("Filter schedule 2 pump speed"), default=0, choices=PUMP_SPEEDS)

    @property
    def active_days(self):
        if not self.filterschedule2_enabled:
            return None
        days = []
        days.append('Mon') if self.filterschedule2_monday else None
        days.append('Tue') if self.filterschedule2_tuesday else None
        days.append('Wed') if self.filterschedule2_wednesday else None
        days.append('Thu') if self.filterschedule2_thursday else None
        days.append('Fri') if self.filterschedule2_friday else None
        days.append('Sat') if self.filterschedule2_saturday else None
        days.append('Sun') if self.filterschedule2_sunday else None
        return ', '.join(days)

    def pump_speed_str(self):
        try:
            return PUMP_SPEEDS[self.filterschedule2_pump_speed][1]
        except:
            return ''


class SettingsFilterSchedule3Model(models.Model):
    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='settings_filterschedule3',
                                       null=True)
    depends_on = 'io_control_available'
    formname = 'SettingsFilterSchedule3Form'
    objects = models.Manager()

    filterschedule3_enabled = models.BooleanField(_("Filter schedule 3 enabled"), default=False)
    filterschedule3_start_time = models.TimeField(_("Filter schedule 3 start time"),
                                                  default=datetime.utcfromtimestamp(0))
    filterschedule3_stop_time = models.TimeField(_("Filter schedule 3 stop time"), default=datetime.utcfromtimestamp(0))
    filterschedule3_monday = models.BooleanField(_("Filter schedule 3 monday"), default=False)
    filterschedule3_tuesday = models.BooleanField(_("Filter schedule 3 tuesday"), default=False)
    filterschedule3_wednesday = models.BooleanField(_("Filter schedule 3 wednesday"), default=False)
    filterschedule3_thursday = models.BooleanField(_("Filter schedule 3 thursday"), default=False)
    filterschedule3_friday = models.BooleanField(_("Filter schedule 3 friday"), default=False)
    filterschedule3_saturday = models.BooleanField(_("Filter schedule 3 saturday"), default=False)
    filterschedule3_sunday = models.BooleanField(_("Filter schedule 3 sunday"), default=False)
    filterschedule3_pump_speed = models.IntegerField(_("Filter schedule 3 pump speed"), default=0, choices=PUMP_SPEEDS)

    @property
    def active_days(self):
        if not self.filterschedule3_enabled:
            return None
        days = []
        days.append('Mon') if self.filterschedule3_monday else None
        days.append('Tue') if self.filterschedule3_tuesday else None
        days.append('Wed') if self.filterschedule3_wednesday else None
        days.append('Thu') if self.filterschedule3_thursday else None
        days.append('Fri') if self.filterschedule3_friday else None
        days.append('Sat') if self.filterschedule3_saturday else None
        days.append('Sun') if self.filterschedule3_sunday else None
        return ', '.join(days)

    def pump_speed_str(self):
        try:
            return PUMP_SPEEDS[self.filterschedule3_pump_speed][1]
        except:
            return ''


class SettingsRxModel(models.Model):
    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='settings_rx', null=True)
    formname = 'SettingsRxForm'
    objects = models.Manager()

    rx_value_target = FloatRangeField(_("Desired Rx value (mV)"), default=0.0, min_value=0, max_value=999)
    rx_value_target_ppm = FloatRangeField(_("Desired Rx value (ppm)"), default=0.0, min_value=0, max_value=5)
    rx_dosing_time = IntegerRangeField(_("Dosing time Rx (s)"), default=0, min_value=0, max_value=3600)
    rx_pausing_time = IntegerRangeField(_("Pause time (min)"), default=0, min_value=0, max_value=999)
    rx_overdose_alert = IntegerRangeField(_("Overdose alarm (l / 4h)"), default=0, min_value=0, max_value=65)
    rx_min_water_temp = FloatRangeField(_("Threshold water temperature (°C)"), default=0.0, min_value=0.0, max_value=99)

    def save(self, *args, **kwargs):
        self.full_clean()  # This ensures model validation is done (min_value, max_value, max_length)
        super().save(*args, **kwargs)


class SettingsPhModel(models.Model):
    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='settings_ph', null=True)
    formname = 'SettingsPhForm'
    objects = models.Manager()

    ph_value_target = FloatRangeField(_("Desired pH value"), default=7.0, min_value=4, max_value=9)
    ph_dosing_time = IntegerRangeField(_("Dosing time pH (s)"), default=100, min_value=0, max_value=3600)
    ph_pausing_time = IntegerRangeField(_("Pausing time pH (min)"), default=100, min_value=0, max_value=1440)
    ph_dosing_choice = models.IntegerField(_("Dosing choice pH"), default=0, choices=PH_CHOICES)
    ph_overdose_alert = IntegerRangeField(_("Overdose Alarm (l / 4h)"), default=65, min_value=0, max_value=65)
    ph_hysteresis = FloatRangeField(_("Hysteresis"), default=0, min_value=0, max_value=1)

    def save(self, *args, **kwargs):
        self.full_clean()  # This ensures model validation is done (min_value, max_value, max_length)
        super().save(*args, **kwargs)


class SettingsFilterModel(models.Model):
    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='settings_filter', null=True)
    formname = 'SettingsFilterForm'
    depends_on = 'io_control_available'
    objects = models.Manager()

    filter_pump_force_on = models.BooleanField(_("Filter pump force on"), default=False)


class SettingsWaterSuppletionModel(models.Model):
    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='settings_watersuppletion',
                                       null=True)
    depends_on = 'water_level_sensor_available'
    objects = models.Manager()

    # watersuppletion_regulation = models.BooleanField(_("Water suppletion regulation"), null=True, default=False) #disable
    watersuppletion_flow_valve = models.BooleanField(_("Use flow input"), null=True, default=False)


class SettingsDeckModel(models.Model):
    """
    Covco = cover control (nieuwe kast die deck beheert)
    Daarmee kun je open|close|stop.
    """

    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='settings_deck', null=True)
    depends_on = 'covco_deck_available'
    formname = 'SettingsCovcoDeckForm'
    objects = models.Manager()

    deck_open = models.BooleanField(_("Deck open"), default=False)
    deck_close = models.BooleanField(_("Deck close"), default=False)
    deck_stop = models.BooleanField(_("Deck stop"), default=False)

    def poolname(self):
        return self.poolsetting.poolname

    def __str__(self):
        return str(self.poolsetting)


class SettingsEnergytool(models.Model):
    """
    Energytool settings
    aan -> zet SettingsTemperaturemodel.temperature_water_target  op een temperatuur
    # todo luchttemperatuur check: minimum luchttemperatuur 14 / 6 graden
    """

    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='settings_energytool',
                                       null=True)
    formname = 'SettingsEnergytoolForm'
    objects = models.Manager()

    energytool_enabled = models.BooleanField(_("Energytool enabled"), default=False)
    minimum_water_temperature = FloatRangeField(_('Minimum water temperature (°C)'), min_value=0, default=0,
                                                max_value=30, help_text=_(
            "Heating always activates when water temperature below this minimum"))
    cheap_energy = models.FloatField(_('Cheap energy (€/Kwh)'), default=0.15,
                                     help_text=_("Cheap energy will activate the heating towards good temperature"))
    good_temperature = FloatRangeField(_('Good water temperature (°C)'), min_value=0, default=25, max_value=30)
    very_cheap_energy = models.FloatField(_('Very cheap energy (€/Kwh)'), default=0.10, help_text=_(
        "Very cheap energy will activate the heating towards GREAT water temperature"))
    great_temperature = FloatRangeField(_('Great water temperature (°C)'), min_value=0, default=28, max_value=30)

    def save(self, *args, **kwargs):
        self.full_clean()  # This ensures model validation is done (min_value, max_value, max_length)
        super().save(*args, **kwargs)


class LogModel(models.Model):  # unused

    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='logging', null=True)
    objects = models.Manager()

    log_main = models.TextField(_("Main log"), max_length=100000)
    log_gui = models.TextField(_("GUI log"), max_length=100000)
    log_cloud = models.TextField(_("Cloud log"), max_length=100000)

    def __str__(self):
        return str(self.poolsetting)


class ConnectEvent(models.Model):
    poolsetting = models.ForeignKey(PoolSetting, on_delete=models.CASCADE, related_name='connect_event', null=True)
    objects = models.Manager()

    ip = models.CharField(max_length=230, db_index=True)
    count = models.IntegerField(default=0)
    first_time = models.DateTimeField(default=now)
    last_time = models.DateTimeField(default=now)


class PoolSpecificUpdate(models.Model):
    poolsetting = models.OneToOneField(PoolSetting, on_delete=models.CASCADE, related_name='pool_specific_update',
                                       null=True)
    is_dirty = models.BooleanField('Dirty', default=False, editable=False)  # Flag that it has been changed
    objects = models.Manager()

    gui_version = models.CharField(_('New Gui version'), max_length=10)
    main_version = models.CharField(_('New Main version'), max_length=10)
    io_version = models.CharField(_('New IO version'), max_length=10)
    eh_version = models.CharField(_('New EH version'), max_length=10)
    wl_version = models.CharField(_('New WL version'), max_length=10)
    deck_version = models.CharField(_('New Deck version'), max_length=10)

    def __str__(self):
        return str(self.poolsetting)