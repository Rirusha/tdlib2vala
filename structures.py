# Copyright (C) 2024 Vladimir Vaskov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

HEADER = """/*
 * Copyright (C) {year} {author}
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

// THIS FILE WAS GENERATED, DON'T MODIFY IT"""

REGULAR_PROPERTY = '    public {0} {1} {{ get; set; {2}}}\n'
 
PROPERTY = '    public {0} {1} {{ get; construct set; {2}}}\n'

INTERNAL_PROPERTY = '    internal {0} {1} {{ get; set; {2}}}\n'

ABSTRACT_CLASS_DEFINITION = 'public abstract class {0}.{1} : {2}'

CLASS_DEFINITION = 'public class {0}.{1} : {2}'

INTERNAL_CLASS_DEFINITION = 'internal class {0}.{1} : {2}'

CLIENT_CLASS = 'public sealed class {namespace}.Client : Object'

METHOD = '    public {type_}{return_type} {name} ({argvn}) {errors}{{{body}}}'

CONSTRUCT = '    construct {\n\n    }\n'

CLIENT_ID = '    public int client_id { get; private set; }'

REQ_MANAGER = '    internal RequestManager request_manager { get; set; }'

CONSTRUCTOR = '    public {constructor_name} ({args}) {{\n        Object ({o_args});\n    }}\n'

ARG = '{arg_type} {name}{default}'

CLIENT_CONSTR = """
    public Client (double timeout = 1.0) {
        Object (timeout: timeout);
    }
"""

CLIENT_FINAL = """
    ~Client () {
        if (request_manager != null) {
            request_manager.stop ();
        }
    }
"""

INIT_BODY = """
        client_id = TDJsonApi.create_client_id ();
        request_manager = new RequestManager (this, timeout);
        request_manager.run.begin (() => {
            version = ((OptionValueString) get_option_sync ("version")).value;  
        });
"""

BODY = """
        try {{

        var obj = new {target_obj} ({args});
        string json_response = "";

        string json_string = TDJsoner.serialize (obj, Case.SNAKE);

        GLib.debug ("send %d %s", client_id, json_string);

        ulong conid = request_manager.recieved.connect ((request_extra, response) => {{
            if (request_extra == obj.tdlib_extra) {{
                json_response = response;
                Idle.add ({func_name}.callback);
            }}
        }});
        TDJsonApi.send (client_id, json_string);

        yield;
        SignalHandler.disconnect (request_manager, conid);

        var jsoner = new TDJsoner (json_response, {{ "@type" }}, Case.SNAKE);
        string tdlib_type = jsoner.deserialize_value ().get_string ();

        if (tdlib_type == "error") {{
            jsoner = new TDJsoner (json_response, {{ "message" }}, Case.SNAKE);
            throw new TDLibError.COMMON (jsoner.deserialize_value ().get_string ());
        }}

        jsoner = new TDJsoner (json_response, null, Case.SNAKE);
        return ({return_type}) jsoner.deserialize_object (null);

        }} catch (JsonError e) {{
            throw new TDLibError.COMMON ("Error while parsing json");
        }}
"""

CASE = '            case "{case}":\n                return ({return_type}) jsoner.deserialize_object ("TDLib{return_type}");'

SYNC_BODY = """
        try {{

        var obj = new {target_obj} ({args});

        string json_string = TDJsoner.serialize (obj, Case.SNAKE);

        GLib.debug ("execute %s", json_string);

        string json_response = TDJsonApi.execute (json_string);

        var jsoner = new TDJsoner (json_response, {{ "@type" }}, Case.SNAKE);
        string tdlib_type = jsoner.deserialize_value ().get_string ();

        if (tdlib_type == "error") {{
            jsoner = new TDJsoner (json_response, {{ "message" }}, Case.SNAKE);
            throw new TDLibError.COMMON (jsoner.deserialize_value ().get_string ());
        }}

        jsoner = new TDJsoner (json_response, null, Case.SNAKE);
        return ({return_type}) jsoner.deserialize_object (null);

        }} catch (JsonError e) {{
            throw new TDLibError.COMMON ("Error while parsing json");
        }}
"""

REQ_MANAGER_CLASS = """
internal sealed class TDLib.RequestManager : Object {{

    public Client client {{ get; construct; }}

    public double timeout {{ get; construct set; }}

    public signal void recieved (string request_extra, string response_json);

    bool keep_running = true;

    public RequestManager (Client client, double timeout) {{
        Object (
            client: client,
            timeout: timeout
        );
    }}

    public async void run () {{
        while (keep_running) {{
            string? json_response = TDJsonApi.receive (timeout);
            if (json_response != null) {{
                try {{
                    TDJsoner jsoner = new TDJsoner (json_response, {{ "@extra" }}, Case.SNAKE);
                    string tdlib_extra = jsoner.deserialize_value ().get_string ();

                    recieved (tdlib_extra, json_response);

                }} catch (JsonError e) {{
                    TDJsoner jsoner = new TDJsoner (json_response, {{ "@type" }}, Case.SNAKE);
                    string tdlib_type = jsoner.deserialize_value ().get_string ();

                    if (tdlib_type.has_prefix ("update")) {{
                        client.update_recieved (deserialize_update (json_response));
                    }} else {{
                        warning ("%s: %s", e.message, json_response);
                    }}
                }}
            }}

            Idle.add (run.callback, Priority.LOW);
            yield;
        }}
    }}

    public Update deserialize_update (string json_string) {{
        var jsoner = new TDJsoner (json_string, null, Case.SNAKE);
        return (Update) jsoner.deserialize_object (null);
    }}

    public void stop () {{
        keep_running = false;
    }}
}}
"""
