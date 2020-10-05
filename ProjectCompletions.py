import sublime_plugin

class ProjectCompletions(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        if view.window() and view.window().project_data():
            completions = view.window().project_data().get("completions")

            if isinstance(completions, list):
                return parse_completions(completions)
            elif isinstance(completions, dict):
                result = []
                for selector in completions:
                    if all_match(view, locations, selector):
                        result += parse_completions(completions[selector])
                return result

        return None

def parse_completions(completions):
    result = []
    for item in completions:
        if len(item) > 1:
            item = [item[0], ''.join(item[1:])]
            result += [item]
    return result

def all_match(view, locs, selector):
    for loc in locs:
        if selector != view.scope_name(loc).rstrip():
            return False
    return True
