import React from "react";

function GoalCard({goal}) {
  return (
    <div className="mt-5">
      <div className="h-[220px] w-[350px] md:w-[600px] bg-white shadow-2xl shadow-[#A5B4FC] rounded-2xl">
        <div className="flex justify-between gap-2 px-3 py-2 mb-4">
          <div>
            <h1 className="md:text-3xl font-myfamily myfontdesign">{goal.target_amount}$</h1>
          </div>
          <div className="flex">
            <div className={`rounded-2xl flex flex-wrap justify-center items-center px-2 mx-2 ${goal.goal_type === 'income'? 'bg-shobuj' : 'bg-laal'}`}>
              <p className="font-myfamily">{goal.goal_type}</p>
            </div>
            <div className="bg-maati rounded-2xl flex flex-wrap justify-center items-center px-2">
              <p>{goal.period}</p>
            </div>
          </div>
        </div>
        <div className="flex justify-around w-3/4 mx-auto">
          <div>
            {/* For TSX uncomment the commented types below */}
            <div
              className="radial-progress text-gray-800 bg-mycolor text-2xl"
              style={
                {
                  "--value": parseInt(goal.get_goal_percentage, 10),
                  "--size": "8rem",
                } /* as React.CSSProperties */
              }
              aria-valuenow={goal.get_goal_percentage}
              role="progressbar"
            >
              {goal.get_goal_percentage}%
            </div>
          </div>
          <div>
            <div className="px-3">
              <p className="mt-3">Remaining: {goal.remaining_amount}</p>
              <p className="mt-3">Start: {goal.start_date}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default GoalCard;
