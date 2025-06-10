import React from 'react'

function GoalHistoryCard({gh}) {
  return (
    <div>
      <div className="h-[200px] w-[300px] md:w-[300px] bg-white shadow-2xl shadow-[#A5B4FC] rounded-2xl">
        <div className="flex justify-between gap-2 px-3 py-2">
          <div>
          <h1 className="md:text-3xl font-myfamily myfontdesign">{gh.target_amount}$</h1>
          </div>
          <div className={`px-4 rounded-xl flex items-center justify-center ${gh.goal_type ==='income' ? 'bg-shobuj': 'bg-laal'}`}>
            <p className="font-myfamily">{gh.goal_type}</p>
          </div>
        </div>
        <div className="mt-4 px-3">
          <h1>Achieved On: {gh.achieved_on}</h1>
        </div>
        <div className="mt-4 px-3">
          <h1>Days taken: {gh.days_taken}</h1>
        </div>
        <div className="mt-4 px-3">
          <p>Start Day: {gh.start_date}</p>
        </div>
      </div>
    </div> 
  )
}

export default GoalHistoryCard
