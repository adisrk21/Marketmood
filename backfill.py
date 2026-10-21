from services.updater import update
if __name__=='__main__':
    x=update(backfill=True,notify=False); print('Backfill complete:',x.to_dict())
