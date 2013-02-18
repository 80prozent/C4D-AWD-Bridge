C4D-AWD-Bridge
==============

A collection of plug-ins for Cinema 4D, that allow importing and exporting of AWD2 files for use with the Away3D engine.

Disclaimer: 

 - Use at your own risk.
 - This code is WIP (Work In Progress)
 - As a starting point for this Plugin, I used some of the "Demo-Plugins" found at http://www.smart-page.net/blog/ (a ressource for c4d-python-development)

License:

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Installation: 

 - copy folder "AWDBridge" into c4d-plugins folder. Done!

Notes:

 - The plugin expects all textures to be in the same folder as the c4d-project-file or in the "tex" folder.
- To avoid any problems with textures, just do "save Project with assets" in c4d, and you are ready to go.
 - To prevent a specific object (and optionally its children) from getting exported, you can apply a "AWDObjectSettings" tag to this object.
 - All unsupported Object-types will be exported as Null-Objects (ObjectContainer3d)
 - To export Skeleton-Binding Data, you need to apply a "AWDSkeleton"-Tag to the root Joint (of the Joints that are bound to your character)
 - To export a Skeleton-Animation, you need to have a copy of your bound Joints, holding the keyframe data. 
- Instead of a "AWDSkeleton"-Tag, this root Joint needs to have a "AWDSkeletonAnimation"-Tag applied.
- Inside the "AWDSkeletonAnimation"-Tag, you can name the Animation.
- To allow animation-export, you need to set a Range inside of the plugin.
- When exporting Skeleton-Animation, the KeyFrames of the Root-Joint of the animated Joint-structure defines the KeyFrames of the exported animation (e.g. if all joints have a keyframe set at a frame, but the root-joint doesnt, no keyframe is exported at this frame. If the root-joint has ne keyframes at all, no animation is exported)
- Only exported Textures are the ones in the Color-Channels


Please send any feedback to: 80prozent@differentdesign.de

