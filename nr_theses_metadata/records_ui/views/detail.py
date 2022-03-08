from functools import wraps

from flask import render_template, g

from nr_theses_metadata.proxies import current_service


def pass_record(f):
    """Decorate a view to pass the latest version of a record."""

    @wraps(f)
    def view(**kwargs):
        pid_value = kwargs.get('pid_value')
        record_latest = current_service.read(
            id_=pid_value, identity=g.identity
        )
        kwargs['record'] = record_latest
        return f(**kwargs)

    return view


@pass_record
def record_detail(record=None, pid_value=None):
    """Record detail page (aka landing page)."""
    # record_ui = UIJSONSerializer().serialize_object_to_dict(record.to_dict())
    record_ui = record.to_dict()
    record_ui['ui'] = {}

    return render_template(
        "nr_theses_metadata/records/detail.html",
        record=record_ui,
        pid=pid_value
    )
