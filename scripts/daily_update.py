from services.updater import update
if __name__=='__main__':
    x=update(backfill=False,notify=True); print(x.to_dict())
