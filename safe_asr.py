import os, shutil
import beautifuldiscord.app as bd

class SafeASR():
  backup_path = './core_backup.asar'# bd uses original_core.asar,
  # core_backup.asar avoids name conflicts and thus bd potentially overwriting a backup

  @staticmethod
  def extract_asr() -> bool:
  # check if an in-progress extraction exists
    if os.path.exists('./core'):
      if os.path.exists(SafeASR.backup_path):
        print('core.asar was previously extracted but not repacked, restoring backup asar')
        shutil.rmtree('./core')
        shutil.move(SafeASR.backup_path, './core.asar')
      else:
        print('core.asar was previously extracted and no backup exists, your Discord client may be broken') # TODO: add better instructions on what to do for recovery
      return False 
    
    # if no backup exists, create one
    if not os.path.exists(SafeASR.backup_path):
      shutil.copyfile('./core.asar', SafeASR.backup_path)
    
    # extract core.asr -> core
    print('extracting core.asr')
    with bd.Asar.open('./core.asar') as f:
      f.extract('./core')
    return True
  
  @staticmethod
  def restore_backup() -> bool:
    try:
        shutil.move(SafeASR.backup_path, './core.asar')
    except FileNotFoundError as e:
        print('no core.asar backup exists')
    else:
        print('restored core.asar from backup')
