C4D-AWD-Bridge
==============

A collection of plugins for Cinema 4D, that allow importing and exporting of AWD2 files for use with the Away3D engine.

Disclaimer: 
 - Use at your own risk.
 - This code is WIP (Work In Progress)

Install: 
 - copy folder "AWDBridge" into c4d-plugins folder. Done!

Notes:
 - The plugin expects all textures to be in the same folder as the c4d-project-file or in the "tex" folder.
	 - To avoid any problems with textures, just do "save Project with assets" in c4d, and you are raedy to go.
 - To prevent a specific object (and optionally its children) from getting exported, you can apply a "AWDObjectSettings" tag to this object.
 - All unsupported Object-types will be exported as Null-Objects (ObjectContainer3d)
 - To export Skeleton-Binding Data, you need to apply a "AWDSkeleton"-Tag to the root Joint (of the Joints that are bound to your character)
 - To export a Skeleton-Animation, you need to have a copy of your bound Joints, holding the keyframe data. 
	 - Instead of a "AWDSkeleton"-Tag, this root Joint needs to have a "AWDSkeletonAnimation"-Tag applied.
	 - Inside the "AWDSkeletonAnimation"-Tag, you can name the Animation.
	 - To allow animation-export, you need to set a Range inside of the plugin.
 - Only Color and Color-Texture are exported


Send feedback to: 80prozent@differentdesign.de