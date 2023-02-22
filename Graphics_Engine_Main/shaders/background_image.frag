#version 330 core
out vec4 fragColor;

in vec4 clipCoords;

uniform sampler2D u_texture_skybox;
//uniform mat4 m_invProjView;


void main() {
//    vec4 worldCoords = m_invProjView * clipCoords;
//    vec3 texCubeCoord = normalize(worldCoords.xyz / worldCoords.w);
    fragColor = texture(u_texture_skybox, clipCoords.xy/2+vec2(0.5,0.5));
//    fragColor = vec4(vec3(clipCoords.x, clipCoords.y, 1), 1);
}