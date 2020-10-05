import sublime_plugin

def all_match(view, locs, selector):
    for loc in locs:
        if selector != view.scope_name(loc).rstrip():
            return False
    return True

class ProjectCompletions(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        if view.window() and view.window().project_data():
            completions = view.window().project_data().get("completions")
            if isinstance(completions, list):
                return completions

            elif isinstance(completions, dict):
                result = []
                for selector in completions:
                    if all_match(view, locations, selector):

                        parse_completions = []
                        for item in completions[selector]:
                            if len(item) > 1:
                                item = [item[0], ''.join(item[1:])]
                                parse_completions += [item]

                        result += parse_completions

                return result
        return None
