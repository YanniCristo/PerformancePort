from dash import html, Input, Output, State, callback_context, no_update, ctx
from db.database import save_info, update_user_password
from flask_login import current_user

def register(app):

    # ── Callback: apre il modal e popola i campi ─────────────────
    @app.callback(
        Output("settings-modal", "is_open"),
        Output("settings-avatar", "children"),
        Output("settings-email", "children"),
        Output("settings-badge", "children"),
        Output("settings-plan-info", "children"),

        Output("settings-name-field", "value"),
        Output("settings-surname-field", "value"),
        Output("settings-country-field", "value"),
        Output("settings-dob-field", "date"),
        Output("settings-phone-field", "value"),
        Output("settings-gender-field", "value"),
        
        Input("open-settings-btn", "n_clicks"),
        Input("settings-modal", "is_open"),
        State("settings-modal", "is_open"),
        prevent_initial_call=True,
    )
    def toggle_settings(n_clicks, _is_open_trigger, is_open):
        from dash import ctx

        no_update_ALL = (False, no_update, no_update, no_update, no_update, no_update,
                         no_update, no_update, no_update, no_update, no_update)
 
        if ctx.triggered_id == "settings-modal":
            return no_update_ALL
 
        if not n_clicks:
            return no_update_ALL
 
        email = current_user.email
        initials = email[:2].upper()
 
        is_pro = current_user.is_paid
        badge = html.Span(
            "PRO" if is_pro else "FREE",
            className=f"sm-badge {'sm-badge--pro' if is_pro else 'sm-badge--free'}")
 
        plan_label = "PRO — abbonamento attivo" if is_pro else "Piano gratuito"

        name        = current_user.name
        surname     = current_user.surname
        country     = current_user.country
        number      = current_user.number
        birthday    = current_user.birthday
        birthday_str = birthday.strftime("%Y-%m-%d") if birthday else None
        gender      = current_user.gender
 
        return (True, initials,
                email,
                badge, plan_label,
                name or "", surname or "",
                country or "", birthday_str or "",
                number or "", gender or "")


    # ── Callback: aggiorna icone tema al toggle ───────────────────
    @app.callback(
        Output("sm-icon-light", "className"),
        Output("sm-icon-dark", "className"),
        Input("settings-theme-toggle", "value"),
    )
    def update_theme_icons(is_dark):
        base = "sm-theme-icon"
        active = "sm-theme-icon sm-theme-icon--active"
        return (base if is_dark else active), (active if is_dark else base)
    
    # ── Callback: apre il modal e popola i campi ─────────────────
    @app.callback(
        Output("settings-save-dummy", "children"),

        # ── Inputs che scatenano il salvataggio ──
        Input("settings-name-field",    "n_blur"),
        Input("settings-surname-field", "n_blur"),
        Input("settings-country-field", "n_blur"),
        Input("settings-phone-field",   "n_blur"),
        Input("settings-dob-field",     "date"),
        Input("settings-gender-field",  "value"),
        
        # ── Valori attuali dei campi (letti come State) ──
        State("settings-name-field",    "value"),
        State("settings-surname-field", "value"),
        State("settings-country-field", "value"),
        State("settings-phone-field",   "value"),
        prevent_initial_call=True,
    )
    def update_info(
        _blur_name, _blur_surname, _blur_country, _blur_phone,
        dob, gender,
        name, surname, country, phone):

        # Mappa: triggered_id → (chiave per save_info, valore da salvare)
        # Le chiavi corrispondono alla whitelist ALLOWED_FIELDS in database.py
        field_map = {
            "settings-name-field":    ("name",     name),
            "settings-surname-field": ("surname",  surname),
            "settings-country-field": ("country",  country),
            "settings-phone-field":   ("number",   phone),
            "settings-dob-field":     ("birthday", dob),
            "settings-gender-field":  ("gender",   gender),
        }
        
        triggered_id = ctx.triggered_id
        if triggered_id not in field_map:
            return no_update

        if triggered_id == "settings-gender-field":
            if gender == (current_user.gender or ""):
                return no_update

        if triggered_id == "settings-dob-field":
            db_dob = current_user.birthday
            db_dob_str = db_dob.strftime("%Y-%m-%d") if db_dob else None
            if dob == db_dob_str:
                return no_update
 
        field, value = field_map[triggered_id]
        save_info(user_id=current_user.id, field=field, value=value)
 
        return no_update

    # ── Callback: bottone Modifica → mostra tab cambio password ────
    @app.callback(
        Output("settings-tabs", "active_tab"),
        Input("settings-chg-pass-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def show_change_password_tab(n_clicks):
        if not n_clicks:
            return no_update
        return "tab-chg-pass"

    # ── Callback: salvataggio nuova password ─────────────────────
    @app.callback(
        Output("chg-pass-feedback", "children"),
        Output("chg-pass-feedback", "style"),
        Input("chg-pass-save-btn", "n_clicks"),
        State("chg-pass-old-pass", "value"),
        State("chg-pass-new-pass", "value"),
        State("chg-pass-new-pass-c", "value"),
        prevent_initial_call=True,
    )
    def save_new_password(n_clicks, old_pass, new_pass, new_pass_c):
        if not n_clicks:
            return no_update, no_update

        # Validazione lato client
        if not old_pass or not new_pass or not new_pass_c:
            return "Compila tutti i campi.", {"color": "red"}

        if new_pass != new_pass_c:
            return "Le nuove password non coincidono.", {"color": "red"}

        if len(new_pass) < 6:
            return "La password deve essere di almeno 8 caratteri.", {"color": "red"}

        result = update_user_password(
            user_id=current_user.id,
            old_password=old_pass,
            new_password=new_pass,
        )

        if result["success"]:
            return "Password aggiornata con successo.", {"color": "green"}
        return result.get("error", "Errore sconosciuto."), {"color": "red"}
