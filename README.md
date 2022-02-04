# UA Schedule-Builder

## General Usage
This program allows users to create a list of courses which can be organized into random optimized schedules according to various specifications. Courses can be added by dragging them out of the search column on the left and dropping them into a valid semester. They can be removed by dragging them back to the search column. When hovering over courses, some other courses will appear red, blue, pink, or remain black. The blue courses are those included in the selected course's prerequisites (Note that only some combination of the blue courses is required, not necesarilly all of them. See the course info for specifics), the red courses are the courses which contain the selected course in their prerequisites, and the pink courses are the courses which are able to be swapped with the selected course. To customize the randomized schedules that are generated, courses can be locked into place, meaning that all generated schedules will keep locked courses where they are. Semesters can also be locked, meaning they will not contain any courses in new schedules. Note that locking too many classes/semesters can lead to an impossible course configuration, meaning no new schedules will be generated until the user resolves the issue.

The prerequisites and concurrent prerequisites of courses were automatically scraped from UA's course inventory. Many of these prerequisites have non-course elements such as "permission from course instructor" or "minimum score of 500 on UA mathematics placement exam." Note that these requirements will be treated as courses by the program and evaluated as not met. In some cases this will not be an issue because there are other valid combinations of courses that could satisfy the course's prerequisites. If it does lead to a problem, however, these irregular statements can simply be removed in the course csv file so long as the user stays aware that the requirement still applies in reality. A list of all prerequisites to all courses currently active can be printed to the console to check for such cases.

The two files accompanying the main program, MyCourses.txt and CompletedCourses.txt, store the course data. MyCourses stores the courses that appear on screen when the program is first opened and is the where they are saved to when it closes. CompletedCourses stores the courses that are to be counted as completed for all prerequisites but not shown on screen. These can include course credits earned through AP classes for example. Both files store the courses by name in a comma separated (comma without a space) list including a comma at the end.

## Keyboard Controls
- Escape:
  - Exits an information block if one if currently displayed
  - Exits the program and saves the current courses
  - Shift: Exits the program without saving the current courses
- Enter: Generates a new, randomized schedule
- Tab: Creates or exits an information block of the course being hovered over
- L-Alt: 
  - Selects a course to switch with another if none is selected
  - Switches the selected course with the hovered course if the hovered course is highlighted pink (meaning there are no prerequisite conflicts) 
- Delete: Clears the search field
- Shift P: Prints every course's prerequisites and concurrent prerequisites to the console
- Up: Increments the maximum number of courses per semester (default is 16)
- Down: Decrements the maximum number of courses per semester
- Right: Increments the maximum number of semesters (default is 8)
- Left: Decrements the maximum number of semesters

## Mouse Controls
- Left Click:
  - Drags the selected course to valid semesters or deletes them if dropped in the search column
  - Creates a new course object from the clicked course in the search column
  - Drags the scroll bar to quickly locate courses in the search column
  - Shift: Toggles the lock on the selected course in its current semester
- Right Click:
  - Toggles the lock on the selected course in its current semester
  - Toggles the lock on the selected semester column
- Scroll Wheel: scrolls through course results in the search column or any information block being displayed

## Required Libraries
- pygame
