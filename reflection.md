# PawPal+ Project Reflection

## 1. System Design

- User should be able to add a pet, add tasks, and be able to properly view all tasks added.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

- My inital UML design was to have the Owner class have a Schedule class that holds all the tasks as well as an attribute to hold available time throughout a day and methods to assingn tasks accordingly. Each task has an attribute that has it set to completed or not based on if that task has been checked off as complete with the accompaning method. The Pet class keeps track of all the pets currently in the system as well as their dietary and medication needs.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

- Yes, Copilot pointed out there wasn't a clear relationship between the Pet class and the Task Class. If kept this way going forward implemnting an algorithm pertaining to prioritzaion in the scheduler would add levels of unecssary complexity.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

- My scheduler consider time an priority. Time is a given since as a scheduler the time when tasks should start is important for a user to be constantly aware of. As for priority there will always be measure of importance that needs to be considered and giving them the ability to assing priority helps them consider such implications

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

- Scheduler does not take into account the duration of tasks. At most checking if there is an exact time overlap. This reasoanble in this scenario because the processing time it would take to calc all the overlap of times will be in poly which I don't want. I want most of the functions  to be in linear if possible.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
