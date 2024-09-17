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