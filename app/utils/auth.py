from functools import wraps

from flask import abort, jsonify, redirect, request, session, url_for


def require_roles(*allowed_role_ids):
    def decorator(view_function):
        @wraps(view_function)
        def wrapped_view(*args, **kwargs):
            if "user_id" not in session:
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify({
                        "error": "session_expired",
                        "message": "Oturumunuz sona erdi. Lütfen yeniden giriş yapın."
                    }), 401

                return redirect(url_for("login"))

            if session.get("role_id") not in allowed_role_ids:
                abort(403)

            return view_function(*args, **kwargs)

        return wrapped_view

    return decorator