from ui.app import RecordEditorApp
from middleman.event_handler import EventHandler
from records.record_keeper import RecordKeeper

from records.random_filler import RandomRecordFiller


if __name__ == '__main__':
    record_keeper = RecordKeeper()
    #RandomRecordFiller.fill_keeper(record_keeper, 50)
    RecordEditorApp(EventHandler(record_keeper)).run()
