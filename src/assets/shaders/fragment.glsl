#version 330 core 

in vec3 fragmentColor; 
in vec2 fragmentTexCoord; 

out vec4 color; 

uniform sampler2D imageTexture; 
uniform float time = 0;
uniform float speed = 0.003;

vec2 resolution = vec2(1000, 800);

void main() {
    vec2 cPos = -1.0 + 2.0 * gl_FragCoord.xy / resolution.xy;
    float cLength = length(cPos);
    vec2 uv = gl_FragCoord.xy/resolution.xy+(cPos/cLength)*cos(cLength*12.0-time*4.0)*speed;

    vec4 rand_tex = texture(imageTexture, vec2(0.3, 0.3));
    vec4 noise = mix(texture(imageTexture, uv), vec4(0.0, 0.0, 0.0, 1.0), 0.8);
    vec4 base = mix(texture(imageTexture, uv), vec4(0.0, 0.0, 0.0, 1.0), distance(vec2(0.5, 0.5), gl_FragCoord.xy / vec2(1000, 800)) * 1.7);
    vec4 light_offset = mix(base, noise, distance(vec2(clamp(sin(time), -0.1, 1.0), 0.1), gl_FragCoord.xy / vec2(1000, 800)));
    vec2 offset = uv.xy + 0.004;
    
    // vec4 c = mix(light_offset, base, 0.2);
    // color = mix(c, vec4(0, 0, 1, 1), 0.1);
    color = base;
}