def create_section_title(title):
        titlebar = Text(title) \
                    .scale(0.75) \
                    .to_edge(LEFT, buff=0.5) \
                    .to_edge(DOWN, buff=0.2)

        titlebar_box = Rectangle(color=BLUE, 
                                 width=config.frame_width,
                                 height=0.75,
                                 fill_opacity=1) \
                        .to_edge(DOWN, buff=0)        
        titlebar.move_to(titlebar_box, ORIGIN).to_edge(LEFT, buff=0.5).to_edge(DOWN, 0.2)
        section_titlebar = Group(titlebar_box, titlebar)
        return section_titlebar

def create_slide_content(title: str, content):
    slide_title = Text(title, color=YELLOW).scale(0.75)
    slide_content = VGroup(slide_title, content).arrange(DOWN, buff=0.5)
    return slide_content.to_corner(UL, buff=0.5)
