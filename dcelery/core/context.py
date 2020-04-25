from re import finditer

from core import db


def camel_case_split(identifier):
    matches = finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]


def make_context():
    print('Importing app context')
    models = getattr(db.Model, '_decl_class_registry').values()
    models_dct = {}
    print('loading models')
    _models = {}

    for model in models:
        if isinstance(model, type) and issubclass(model, db.Model):
            models_dct[model.__name__] = model
            _models.setdefault(camel_case_split(model.__name__)[0], []).append(model.__name__)


    def show_models():
        for _, v in sorted(_models.items()):
            print('=========================================================== \n %s' % '\t\n '.join(v))

    from flask import current_app as app
    from flask import request

    def clean_tasks():
        from modules.routines.models import ScheduleBase, PeriodicTask
        for sb in ScheduleBase.query.all():
            db.session.delete(sb)
        for pt in PeriodicTask.query.all():
            db.session.delete(pt)
        db.session.commit()

    context = dict(
        app=app,
        db=db,
        show_models=show_models,
        request=request,
        clean_tasks=clean_tasks,
        **models_dct
    )
    print('app, db, cache instances are available')
    return context
