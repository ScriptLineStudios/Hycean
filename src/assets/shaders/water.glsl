#version 330 core 

in vec3 fragmentColor;
in vec2 fragmentTexCoord; 

out vec4 color; 

uniform sampler2D imageTexture; 
uniform float time = 0;

void main() {
    float pixels = 512.0;
    float dx = 8.0 * (1.0 / pixels);
    float dy = 8.0 * (1.0 / pixels);
    vec2 coord = vec2(dx * floor(fragmentTexCoord.x / dx), dy * floor(fragmentTexCoord.y / dy));

    float rand = coord.x + coord.y;
    vec4 base = texture(imageTexture, (coord));
    
    color = base;
}