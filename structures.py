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

CLIENT_FINAL = """
    ~Client () {
        if (request_manager != null) {
            request_manager.stop ();
        }
    }
"""

INIT_BODY = """
        client_id = TDJsonApi.create_client_id ();
        request_manager = new RequestManager ();
        request_manager.run.begin ();
"""

BODY = """
        var obj = new {target_obj} ({args});
        string json_response = "";

        string json_string = yield TDJsoner.serialize_async (obj, Case.SNAKE);
        
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
            throw new BadStatusCodeError.COMMON (jsoner.deserialize_value ().get_string ());
        }}

        jsoner = new TDJsoner (json_response, null, Case.SNAKE);

        {return_type} out_obj;
        switch (tdlib_type) {{
{cases}
            default:
                assert_not_reached ();
        }}

        return out_obj;
"""

CASE = '            case "{case}":\n                out_obj = ({return_type}) jsoner.deserialize_object (typeof ({return_type}));\n                break;'

SYNC_BODY = """
        var obj = new {target_obj} ({args});

        string json_string = TDJsoner.serialize (obj, Case.SNAKE);

        GLib.debug ("execute %s", json_string);

        string json_response = TDJsonApi.execute (json_string);
        
        var jsoner = new TDJsoner (json_response, {{ "@type" }}, Case.SNAKE);
        string tdlib_type = jsoner.deserialize_value ().get_string ();
        
        if (tdlib_type == "error") {{
            jsoner = new TDJsoner (json_response, {{ "message" }}, Case.SNAKE);
            throw new BadStatusCodeError.COMMON (jsoner.deserialize_value ().get_string ());
        }}

        jsoner = new TDJsoner (json_response, null, Case.SNAKE);

        {return_type} out_obj;
        switch (tdlib_type) {{
{cases}
            default:
                assert_not_reached ();
        }}

        return out_obj;
"""

REQ_MANAGER_CLASS = """
internal sealed class TDLib.RequestManager : Object {

    public signal void recieved (string request_extra, string response_json);

    bool keep_running = true;
    MainLoop? ml = null;

    public async void run () {
        while (keep_running) {
            string? json_response = TDJsonApi.receive (0.05);
            if (json_response != null) {
                TDJsoner jsoner;
                try {
                    jsoner = new TDJsoner (json_response, { "@extra" }, Case.SNAKE);
                } catch (JsonError e) {
                    warning ("%s: %s", e.message, json_response);
                    continue;
                }
                
                string tdlib_extra = jsoner.deserialize_value ().get_string ();

                recieved (tdlib_extra, json_response);
            }

            Idle.add (run.callback, Priority.LOW);
            yield;
        }
    }

    public void stop () {
        keep_running = false;
    }
}
"""
