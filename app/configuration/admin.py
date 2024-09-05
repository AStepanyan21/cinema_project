import json
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import FileUploadField

from app.configuration.database import SyncSessionLocal
from app.configuration.settings import settings
from app.models.cinema import CinemaRoom, Move, MoveTime, Session, OccupiedSeat
from app.utils.constands import MEDIA_FOLDER


class MoveModelView(ModelView):
    column_list = ['name', 'move_time_length', 'movie_cover', ]

    form_overrides = {
        'movie_cover': FileUploadField
    }
    form_args = {
        'movie_cover': {
            'label': 'Movie Cover',
            'base_path': MEDIA_FOLDER,
            'allow_overwrite': False,
            'relative_path': 'media/'
        }
    }


class CinemaRoomModelView(ModelView):
    column_list = ['name', 'column', 'row']

    def on_model_change(self, form, model, is_created):
        if is_created or form.row.data != model.row or form.column.data != model.column:
            seating_matrix = [[False] * form.column.data for _ in range(form.row.data)]
            model.seating = json.dumps(seating_matrix)
        return super().on_model_change(form, model, is_created)


class SessionModelView(ModelView):
    column_list = ['cinema_room', 'move', 'move_time']
    form_columns = ['cinema_room', 'move', 'move_time']
    column_labels = {
        'cinema_room': 'Cinema Room',
        'move': 'Movie',
        'move_time': 'Show Time'
    }


class OccupiedSeatModelView(ModelView):
    column_list = ['session', 'row', 'column']
    form_columns = ['session', 'row', 'column']
    column_labels = {
        'session': 'Session',
        'row': 'Row',
        'column': 'Column'
    }

    def get_query(self):
        return super().get_query()


flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = settings.app_settings.SECRET_KEY

admin = Admin(app=flask_app, name='Cinema Admin', template_mode='bootstrap3')
admin.add_view(CinemaRoomModelView(CinemaRoom, session=SyncSessionLocal()))
admin.add_view(MoveModelView(Move, session=SyncSessionLocal()))
admin.add_view(ModelView(MoveTime, session=SyncSessionLocal()))
admin.add_view(SessionModelView(Session, session=SyncSessionLocal()))
admin.add_view(OccupiedSeatModelView(OccupiedSeat, session=SyncSessionLocal()))

if __name__ == "__main__":
    flask_app.run(debug=True)
