import React, { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Skeleton } from "@/components/ui/skeleton";

import GoalCard from "../components/ui/GoalCard";
import { useGoalStore } from "../../store/useGoalStore";
import GoalHistoryCard from "../components/ui/GoalHistoryCard";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

function Goal() {
  const { loading, goals, goalHistory, fetchGoals, fetchGoalHistory } =
    useGoalStore();

  const [isDialogOpen2, setIsDialogOpen2] = useState(false);
  const [formDatag, setFormDatag] = useState({
    target_amount: "",
    period: "",
    goal_type: "",
  });

  const handleChange2 = (event) => {
    const { name, value } = event.target;
    setFormDatag((prev) => ({
      ...prev,
      [name]: value,
    }));
    console.log(name, value);
  };

  const handleSubmitGoal = async (event) => {
    event.preventDefault();
    const token = localStorage.getItem("access");

    try {
      const res = await fetch("http://127.0.0.1:8000/api/goal/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(formDatag),
      });

      if (!res.ok) {
        throw new Error("goal create failed");
      }
      setIsDialogOpen2(false);
    } catch (error) {
      console.log("failed....");
    }
    setFormDatag({
      target_amount: "",
      period: "",
      goal_type: "",
    });
  };

  useEffect(() => {
    fetchGoals();
    fetchGoalHistory();
    // const interval = setInterval(() => {
    //   fetchGoals();
    //   fetchGoalHistory();
    // }, 10000); // every 10 seconds

    // return () => clearInterval(interval);
  }, []);
  const incomeGoal = goals.filter((goal) => goal.goal_type === "income");
  const expenseGoal = goals.filter((goal) => goal.goal_type === "expense");

  return (
    <div className="container max-w-6xl mx-auto px-4 min-h-screen">
      <div>
        <div className="mb-2">
          <Dialog open={isDialogOpen2} onOpenChange={setIsDialogOpen2}>
            <DialogTrigger asChild>
              <Button
                className="w-full bg-asmani text-xl"
                onClick={() => setIsDialogOpen2(true)}
              >
                create a Goal
              </Button>
            </DialogTrigger>
            <DialogContent className="mydivdesign">
              <DialogHeader>
                <DialogTitle className="text-center text-2xl">Goal</DialogTitle>
                <DialogDescription className="text-center">
                  Artho
                </DialogDescription>
              </DialogHeader>
              <form
                onSubmit={handleSubmitGoal}
                className="flex flex-col md:gap-4 md:mt-4 md:px-30"
              >
                <div className="flex flex-col">
                  <label
                    htmlFor="target_amount"
                    className="mb-1 font-medium myfamily text-gray-800"
                  >
                    Target Amount
                  </label>
                  <input
                    id="target_amount"
                    type="number"
                    placeholder="enter your amount"
                    className="border text-gray-800 border-mycolor rounded-2xl px-3 py-2 focus:outline-none focus:ring-mycolor bg-gray-100"
                    onChange={handleChange2}
                    name="target_amount"
                    value={formDatag.target_amount}
                    required
                  />
                </div>
                <div className="flex flex-col">
                  <label
                    htmlFor="transaction_type"
                    className="mb-1 font-medium myfamily text-gray-800"
                  >
                    Goal_type
                  </label>
                  <select
                    id="goal_type"
                    name="goal_type"
                    value={formDatag.goal_type}
                    onChange={handleChange2}
                    className="border text-gray-800 border-mycolor rounded-2xl px-3 py-2 focus:outline-none focus:ring-mycolor bg-gray-100"
                    required
                  >
                    <option value="">Select type</option>
                    <option value="income">Income</option>
                    <option value="expense">Expense</option>
                  </select>
                </div>
                <div className="flex flex-col">
                  <label
                    htmlFor="period"
                    className="mb-1 font-medium myfamily text-gray-800"
                  >
                    Period
                  </label>
                  <select
                    id="period"
                    name="period"
                    value={formDatag.period}
                    onChange={handleChange2}
                    className="border text-gray-800 border-mycolor rounded-2xl px-3 py-2 focus:outline-none focus:ring-mycolor bg-gray-100"
                    required
                  >
                    <option value="">Select type</option>
                    <option value="daily">Daily</option>
                    <option value="weekly">Weekly</option>
                    <option value="monthly">Monthly</option>
                    <option value="yearly">Yearly</option>
                  </select>
                </div>
                <div>
                  <Button type="submit" className="w-full mt-3">
                    create
                  </Button>
                </div>
              </form>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      <div className="flex flex-col mt-10 items-center">
        <h1 className="text-4xl mb-5">Goals</h1>
        <hr className="border-black border w-1/2" />
      </div>

      <div className="tabing mt-5">
        {loading ? (
          <div className="flex items-center space-x-4 justify-center">
            <Skeleton className="h-12 w-12 rounded-full bg-mycolor" />
            <div className="space-y-2">
              <Skeleton className="h-4 w-[250px] bg-mycolor" />
              <Skeleton className="h-4 w-[200px] bg-mycolor" />
            </div>
          </div>
        ) : (
          <Tabs defaultValue="All" className="flex items-center">
            <TabsList className="mt-3">
              <TabsTrigger value="All">All</TabsTrigger>
              <TabsTrigger value="Income">Income</TabsTrigger>
              <TabsTrigger value="Expense">Expense</TabsTrigger>
              <TabsTrigger value="History">History</TabsTrigger>
            </TabsList>
            <TabsContent value="All">
              {goals.map((goal) => (
                <GoalCard key={goal.id} goal={goal} />
              ))}
            </TabsContent>
            <TabsContent value="Income" className="">
              {incomeGoal.map((goal) => (
                <GoalCard key={goal.id} goal={goal} />
              ))}
            </TabsContent>
            <TabsContent value="Expense" className="">
              {expenseGoal.map((goal) => (
                <GoalCard key={goal.id} goal={goal} />
              ))}
            </TabsContent>
            <TabsContent
              value="History"
              className="w-full grid grid-cols-1 md:grid-cols-3 gap-y-6 justify-items-center"
            >
              {goalHistory.map((gh) => (
                <GoalHistoryCard key={gh.id} gh={gh} />
              ))}
            </TabsContent>
          </Tabs>
        )}
      </div>
    </div>
  );
}

export default Goal;
