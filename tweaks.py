class Tweak:
    def __init__(self, id: str, name: str, description: str, content: str, conflicts: list[str] = None) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.content = content 
        self.conflicts = conflicts if conflicts is not None else []
        self.has_conflicts = len(self.conflicts) > 0


TWEAKS = [
    Tweak(
        "hide_vscode_icon", 
        "Hide VSCode icon", 
        "Hides VSCode icon from top bar", 
        """/* Hide vscode icon */
.monaco-workbench .part.titlebar>.titlebar-container>.titlebar-left>.window-appicon {
    display: none !important;
}"""
    ),
    Tweak(
        "14px_margin_to_topbar",
        "Add 14px margin to topbar",
        "If you hiding vscode icon this tweak is very recommended because many windows in vscode having margin 14px",
        """.monaco-workbench .part.titlebar>.titlebar-container>.titlebar-left>.menubar {
  margin-left: 14px !important;
}"""
    ),
    Tweak(
        "blur_bg_cmd_palette",
        "Blur bg on command palette",
        "Adding blur to bg when opening command palette (control + shift + p)",
        """/** style(command-palette) add blur underlay */
body:has(.quick-input-widget:not([style*="display: none;"])) .monaco-grid-view {
  filter: blur(var(--al-command-palette-blur-amount, 4px)) brightness(70%) !important;
}

/** style(command-palette) remove blur underlay when color theme selection */
body:has(.quick-input-widget .monaco-list[aria-label*="Select Color Theme"]) .monaco-grid-view,
body:has(.quick-input-widget .monaco-list[aria-label*="Select File Icon"]) .monaco-grid-view {
  filter: initial !important;
}"""
    ),
    Tweak(
        "center_tabs",
        "Center opened tabs",
        "Centering opened files tabs",
        """.monaco-workbench .part.editor>.content .editor-group-container>.title .tabs-container {
    justify-content: center !important;
}"""
    ),
    Tweak(
        "dynamic_tabs_size",
        "Dynamic tabs size",
        "Expands tabs on tab line to fill empty space",
        """.monaco-workbench .part.editor>.content .editor-group-container>.title .tabs-container>.tab.sizing-fit[role="tab"] {
    flex: 1 1 300px !important; 
}"""
    ),
    Tweak(
        "center_tab_text",
        "Center text on tabs",
        "Centering text on tabs",
        """/* center text on tabs */
.monaco-workbench .part.editor>.content .editor-group-container>.title .tabs-container>.tab.sizing-fit .monaco-icon-label>.monaco-icon-label-container {
    text-align: center !important;
}"""
    ),
    Tweak(
        "hide_tabs_editor",
        "Hide tabs editor buttons",
        "Hiding run button from tablist and hides split editor (this functions still avaible in View)",
        """/* Hide tabs editor buttons*/
.monaco-workbench .part.editor>.content .editor-group-container>.title .editor-actions {
    display: none !important;
}
"""
    ),
    Tweak(
        "hide_layout_changer_buttons",
        "Hide layout settings from top bar",
        "Hiding buttons thatd just dublicating functional from View",
        """/* Hide right layout icons */
.monaco-workbench .part.titlebar>.titlebar-container>.titlebar-right>.action-toolbar-container .monaco-action-bar .action-item[role="presentation"]{
    display: none !important;
}"""
    ),
    Tweak(
        "hide_left_sidebar_buttons",
        "Hide left sidebar items",
        "Hiding problem and error counter from sidebar, gives opportunity to center right items",
        """.monaco-workbench .part.statusbar>.left-items {
    flex-grow: 0 !important;
    display: none !important;
}"""
    ),
    Tweak(
        "center_right_sidebar_items",
        "Center left sidebar items",
        "Centering right sidebar information",
        """/* Center Right sidebar items */
.monaco-workbench .part.statusbar>.right-items {
    flex-grow: 1 !important;
    justify-content: center !important;
}"""
    ),
    Tweak(
        "hide_center_topbar_label",
        "Hide search panel from top bar",
        "Hiding serach bar from topbar (use control shift p to call commands or delete \">\" symbol from begining of sequence to search)",
        """/* Hide center toolbar */
.monaco-workbench .part.titlebar>.titlebar-container>.titlebar-center>.window-title>.command-center .action-item.command-center-center {
    display: none !important;   
}"""
    ),
    Tweak (
        "hide_new_file_and_folder_btns",
        "Hide new file and new folder buttons from FOLDERS",
        "Hides useless buttons from FOLDERS panel. (Reload button still avaible)",
        """.monaco-workbench .part>.title>.title-actions .action-label[aria-label*="New File..."],
.monaco-workbench .part>.title>.title-actions .action-label[aria-label*="New Folder..."] {
  display: none !important;
}"""
    )
]


def find_tweak_by_id(id: str):
    for tweak in TWEAKS:
        if tweak.id == id:
            return tweak
    return None


class TweaksHandler:
    def __init__(self, tweaks: list[str] = None) -> None:
        self.tweaks = []
        if tweaks:
            for tweak_id in tweaks:
                tweak = find_tweak_by_id(tweak_id)
                if tweak:
                    self.tweaks.append(tweak)
    
    def get_tweak_by_id(self, id: str) -> Tweak:
        for tweak in self.tweaks:
            if tweak.id == id:
                return tweak
        raise ValueError(f"Tweak with ID '{id}' not found")
    
    def get_css_content(self) -> str:
        return "\n".join([tweak.content for tweak in self.tweaks])