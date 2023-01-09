import pygame
import pygame.gfxdraw

def draw_arrow(
        surface: pygame.Surface,
        start: pygame.Vector2,
        end: pygame.Vector2,
        color: pygame.Color,
        head_width: int = 4,
        head_height: int = 2,
    ):

    arrow = start - end
    angle = arrow.angle_to(pygame.Vector2(0, -1))

    # Create the triangle head around the origin
    head_verts = [
        pygame.Vector2(0, head_height / 2),  # Center
        pygame.Vector2(head_width / 2, -head_height / 2),  # Bottomright
        pygame.Vector2(-head_width / 2, -head_height / 2),  # Bottomleft
    ]
    # Rotate and translate the head into place
    translation = pygame.Vector2(0, arrow.length() - (head_height / 2)).rotate(-angle)
    for i in range(len(head_verts)):
        head_verts[i].rotate_ip(-angle)
        head_verts[i] += translation
        head_verts[i] += start

    pygame.gfxdraw.filled_polygon(surface, head_verts, color)
    pygame.gfxdraw.aapolygon(surface, head_verts, color)
