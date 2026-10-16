from services.backup_service import BackupService

print(
    hasattr(
        BackupService,
        "get_backups"
    )
)

print(
    BackupService.get_backups()
)