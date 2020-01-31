# LerntiaControl
**LerntiaControl** is a program to control the learning- and exam-tool **Lerntia** by tracking eyes and face-gestures. It contains two modes: a normal mode and a 2-gestures mode.
### Normal mode
By default, starting the application leads to the normal mode. In this mode, mouse movements are performed by moving the face. For left clicks, the head has to be steady in a defined threshold, until a gray square appears near the mouse cursor on the screen. The gesture that is accomplished right after, is then detected.  If a head-nod is detected while the gray square is near the cursor on the screen, the square turns its color into green and a mouse left click is realized. Otherwise, the square turns its color into red, and no click-action is taken.  
### 2-gestures mode
When the application is in normal mode, the 2-gestures mode is reached through the menu option. In this mode, two gestures are recognized, which are head-nods and head-shakes. A head-nod leads to the actions "click and go", implemented by the `space`+`tab` keys, while a head-shake leads to a "go" action, realized by the `tab` key, as required by **Lerntia**.
## Install and start **LerntiaControl**
* **Install** the application by running `install.bat` or `install.sh`.
* **Start** the application by running `Demo/start.bat` or `Demo/start.sh`.
* A html and pdf **code-documentation** is available in `Doc/code_documentation_html` and `Doc/code_documentation.pdf`.
