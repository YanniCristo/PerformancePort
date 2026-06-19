from dash import Output, Input, State, html, no_update, dcc
from flask_login import current_user
import dash_bootstrap_components as dbc


def settings_modal():
    """Restituisce il componente Modal da includere nel layout principale."""
    return html.Div([
 
        # ── Div nascosto: output "dummy" per la callback update_info ──
        html.Div(id="settings-save-dummy", style={"display": "none"}),

        dbc.Modal(
            id="settings-modal",
            is_open=False,
            centered=True,
            size="md",
            children=[

                # ── Header ──────────────────────────────────────────────
                dbc.ModalHeader(
                    html.Div([
                        html.Div(id="settings-avatar", className="sm-avatar"),
                        html.Div([
                            html.P(id="settings-email", className="sm-email"),
                            html.Span(id="settings-badge"),
                        ])
                    ], className="sm-header-row"),
                    close_button=True,
                ),

                # ── Body con Tabs ────────────────────────────────────────
                dbc.ModalBody(
                    dbc.Tabs(
                        id="settings-tabs",
                        active_tab="tab-info",
                        class_name="sm-tabs",
                        children=[

                            # ── Tab 1: Info ──────────────────────────────
                            dbc.Tab(label="Info", tab_id="tab-info", children=[
                                html.Div(className="sm-tab-body", children=[

                                    dbc.Label("Password", size="sm", className="text-muted"),
                                    html.Div([
                                        dbc.Input(id="settings-Password-field", value='******', disabled=True, class_name="mb-3"),
                                        dbc.Button("Modifica", id="settings-chg-pass-btn", size="sm", outline=True, class_name="sm-inline-edit-btn"),
                                    ], className="sm-field-row"),

                                    dbc.Label("Nome", size="sm", className="text-muted"),
                                    dbc.Input(id="settings-name-field", placeholder="Nome", class_name="mb-3"),

                                    dbc.Label("Cognome", size="sm", className="text-muted"),
                                    dbc.Input(id="settings-surname-field", placeholder="Cognome", class_name="mb-3"),

                                    dbc.Label("Country", size="sm", className="text-muted"),
                                    dbc.Input(id="settings-country-field", placeholder="Country", class_name="mb-3"),

                                    dbc.Label("Data di nascita", size="sm", className="text-muted"),
                                    dcc.DatePickerSingle(
                                        id="settings-dob-field",
                                        placeholder="DD/MM/YYYY",
                                        display_format="DD/MM/YYYY",
                                        first_day_of_week=1,
                                        max_date_allowed="2013-12-31",
                                        initial_visible_month="1990-01-01",
                                        className="mb-3 w-100",
                                    ),

                                    dbc.Label("Telefono", size="sm", className="text-muted"),
                                    dbc.Input(id="settings-phone-field", placeholder="+39 000 000 0000",
                                              type="tel", class_name="mb-3"),

                                    dbc.Label("Genere", size="sm", className="text-muted"),
                                    dbc.Select(
                                        id="settings-gender-field",
                                        options=[
                                            {"label": "Uomo",   "value": "male"},
                                            {"label": "Donna",  "value": "female"}],
                                        value="", class_name="mb-4",
                                    ),
                                ]),
                            ]),

                            # ── Tab 2: Account ───────────────────────────
                            dbc.Tab(label="Account", tab_id="tab-account", children=[
                                html.Div(className="sm-tab-body", children=[

                                    # Riquadro piano attuale
                                    html.Div([
                                        html.Div([
                                            html.P("Piano attuale", className="sm-plan-title"),
                                            html.P(id="settings-plan-info", className="sm-plan-info"),
                                        ]),
                                        dbc.Button(
                                            "Upgrade",
                                            size="sm",
                                            href="/subs",
                                            external_link=True,
                                            class_name="sm-upgrade-btn",
                                        ),
                                    ], className="sm-plan-row"),

                                    html.Hr(className="sm-divider"),
                                ]),
                            ]),

                            # ── Tab 3: Aspetto ───────────────────────────
                            dbc.Tab(label="Aspetto", tab_id="tab-appearance", children=[
                                html.Div(className="sm-tab-body", children=[

                                    html.P("Tema", className="sm-section-title"),
                                    html.Div([
                                        html.Div([
                                            html.Span("Modalità", className="sm-setting-label"),
                                            html.Span("Scegli tra tema chiaro e scuro",
                                                      className="sm-setting-hint"),
                                        ]),
                                        html.Div([
                                            html.Span("☀", id="sm-icon-light",
                                                      className="sm-theme-icon sm-theme-icon--active"),
                                            dbc.Switch(id="settings-theme-toggle", value=False,
                                                       class_name="sm-theme-switch"),
                                            html.Span("☽", id="sm-icon-dark",
                                                      className="sm-theme-icon"),
                                        ], className="sm-theme-toggle-wrap"),
                                    ], className="sm-row"),
                                ]),
                            ]),

                            # ── Tab 4: (Hidden) Cambia Password ───────────────────────
                            dbc.Tab(label="Modifica Password", tab_id="tab-chg-pass", label_style={"display": "none"}, children=[
                                html.Div(className="sm-tab-body", children=[
                                    
                                    dbc.Label("Password attuale", size="sm", className="text-muted"),
                                    dbc.Input(id="chg-pass-old-pass", type="password", placeholder="Password attuale", class_name="mb-3"),

                                    dbc.Label("Nuova Password", size="sm", className="text-muted"),
                                    dbc.Input(id="chg-pass-new-pass", type="password", placeholder="Nuova Password", class_name="mb-3"),

                                    dbc.Label("Conferma Password", size="sm", className="text-muted"),
                                    dbc.Input(id="chg-pass-new-pass-c", type="password", placeholder="Conferma Password", class_name="mb-3"),

                                    html.P(id="chg-pass-feedback", style={"display": "none"}),
                                    dbc.Button("Salva Password", id="chg-pass-save-btn", size="sm", color="primary", class_name="mt-1 w-100"),
                                ])
                            ]),
                        ],
                    )
                ),
            ],
        ),
    ])
