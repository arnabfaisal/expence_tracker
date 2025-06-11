import React, { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { useMemo } from "react";
import { userBalanceStore } from "../../store/userBalanceStore";
import { useTransactionStore } from "../../store/transitionStore";
import { handler } from "../../store/helper";
import LineChart from "../components/Linechart";
import { useCategoryStore } from "../../store/categoryStore";

import { toast } from "sonner";

import { useNavigate } from "react-router-dom";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

// Temporary mock data for the chart

function Dashboard() {
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [isDialogOpen2, setIsDialogOpen2] = useState(false);

  const [formDataTx, setFormDataTx] = useState({
    category_id: 0,
    amount: "",
    description: "",
    transaction_type: "",
  });

  const [formDatag, setFormDatag] = useState({
    target_amount: "",
    period: "",
    goal_type: "",
  });
  const handleChange = (e) => {
    const { name, value } = e.target;

    if (name === "category_id") {
      const selectedCategory = categories.find(
        (cat) => cat.id === Number(value)
      );
      setFormDataTx((prevData) => ({
        ...prevData,
        category_id: value,
        description: selectedCategory?.description || "",
      }));
    } else {
      setFormDataTx((prevData) => ({
        ...prevData,
        [name]: value,
      }));
    }
  };

  const handleChange2 = (event) => {
    const { name, value } = event.target;
    setFormDatag((prev) => ({
      ...prev,
      [name]: value,
    }));
    console.log(name, value);
  };

  const handleSubmitTransaction = async (event) => {
    event.preventDefault();
    const token = localStorage.getItem("access");

    try {
      const res = await fetch("http://127.0.0.1:8000/api/transaction/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(formDataTx),
      });

      if (!res.ok) {
        throw new Error("Registration failed");
      }
      setIsDialogOpen(false);
      fetchbalances();
      fetchtransactions();
      toast.success(
        "Transaction Created: Your transaction was successfully added."
      );
    } catch (error) {
      toast.error("Transaction Failed: Your transaction was failed.");
    }
    setFormDataTx({
      category_id: 0,
      amount: "",
      description: "",
      transaction_type: "",
    });
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
        toast.error("Goal creation failed.");
      }
      setIsDialogOpen2(false);
      toast.success("Goal Created: Your Goal was successfully added.");
    } catch (error) {
      toast.error("Goal creation failed.");
    }
    setFormDatag({
      target_amount: "",
      period: "",
      goal_type: "",
    });
  };

  const { balances, fetchbalances } = userBalanceStore();

  const { transactions, fetchtransactions } = useTransactionStore();
  const { categories, fetchCategories } = useCategoryStore();
  // console.log(transactions);

  useEffect(() => {
    fetchbalances();
    fetchtransactions();
    fetchCategories();

    // const interval = setInterval(() => {
    //   fetchbalances();
    //   fetchtransactions();
    // }, 10000); // every 10 seconds

    // return () => clearInterval(interval);
  }, []);

  const result = useMemo(() => handler(0, transactions), [transactions]);

  const incomeChartData = result.incomeData;
  const expenseChartData = result.expenseData;
  const totalChartData = result.totalData;

  const navigate = useNavigate();

  return (
    <div className="container max-w-6xl mx-auto px-4">
      <section className="twobuttons  mt-5">
        <div>
          <div className="mb-2">
            <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
              <DialogTrigger asChild>
                <Button
                  className="w-full bg-asmani text-xl"
                  onClick={() => setIsDialogOpen(true)}
                >
                  create a Transaction
                </Button>
              </DialogTrigger>
              <DialogContent className="mydivdesign">
                <DialogHeader>
                  <DialogTitle className="text-center text-2xl">
                    Transaction
                  </DialogTitle>
                  <DialogDescription className="text-center">
                    Artho
                  </DialogDescription>
                </DialogHeader>
                <form
                  onSubmit={handleSubmitTransaction}
                  className="flex flex-col md:gap-4 md:mt-4 md:px-30"
                >
                  <div className="flex flex-col">
                    <label
                      htmlFor="amount"
                      className="mb-1 font-medium myfamily text-gray-800"
                    >
                      Amount
                    </label>
                    <input
                      id="amount"
                      type="number"
                      placeholder="enter your amount"
                      className="border text-gray-800 border-mycolor rounded-2xl px-3 py-2 focus:outline-none focus:ring-mycolor bg-gray-100"
                      onChange={handleChange}
                      name="amount"
                      value={formDataTx.amount}
                      required
                    />
                  </div>

                  <div className="flex flex-col">
                    <label
                      htmlFor="transaction_type"
                      className="mb-1 font-medium myfamily text-gray-800"
                    >
                      Transaction Type
                    </label>
                    <select
                      id="transaction_type"
                      name="transaction_type"
                      value={formDataTx.transaction_type}
                      onChange={handleChange}
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
                      htmlFor="category_id"
                      className="mb-1 font-medium myfamily text-gray-800"
                    >
                      Category
                    </label>
                    <select
                      id="category_id"
                      name="category_id"
                      value={formDataTx.category_id}
                      onChange={handleChange}
                      className="border text-gray-800 border-mycolor rounded-2xl px-3 py-2 focus:outline-none focus:ring-mycolor bg-gray-100"
                      required
                    >
                      <option value="">Select category</option>
                      {categories
                        .filter(
                          (cat) => cat.type === formDataTx.transaction_type
                        )
                        .map((category) => (
                          <option key={category.id} value={category.id}>
                            {category.name}
                          </option>
                        ))}
                    </select>
                  </div>
                  <div className="flex flex-col">
                    <label
                      htmlFor="description"
                      className="mb-1 font-medium myfamily text-gray-800"
                    >
                      Category
                    </label>
                    <input
                      id="description"
                      type="text"
                      placeholder="enter description"
                      className="border text-gray-800 border-mycolor rounded-2xl px-3 py-2 focus:outline-none focus:ring-mycolor bg-gray-100"
                      name="description"
                      value={formDataTx.description}
                      onChange={handleChange}
                      required
                    />
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
                  <DialogTitle className="text-center text-2xl">
                    Goal
                  </DialogTitle>
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
      </section>

      <section className="summary mt-5">
        <div className="bg-white h-90 shadow-2xl shadow-[#A5B4FC] rounded-4xl">
          <div className="flex justify-between px-6">
            <div className="mt-5">
              <h1 className="text-2xl font-myfamily font-semibold">Summary</h1>
            </div>
            <div className="flex gap-4 mt-5">
              <Button
                className="bg-asmani md:text-xl text-[10px]"
                id="forgoals"
                onClick={() => {
                  navigate("/goal");
                }}
              >
                Your Goals
              </Button>
              <Button
                className="bg-asmani md:text-xl text-[8px]"
                id="fortx"
                onClick={() => {
                  navigate("/transactions");
                }}
              >
                Your Transactions
              </Button>
            </div>
          </div>

          <div className="flex flex-col w-full px-6 mt-6">
            <div className="bg-maati mt-5 mb-5 h-15 shadow shadow-mycolor rounded-2xl flex flex-col items-center justify-center">
              <h1 className="font-myfamily text-xl">
                Total Balance: {balances[0]?.get_total_balance}${" "}
              </h1>
            </div>
            <div className="bg-shobuj mb-5 h-15 shadow shadow-mycolor rounded-2xl flex flex-col items-center justify-center">
              <h1 className="font-myfamily text-xl">
                Total Income: {balances[0]?.total_income}${" "}
              </h1>
            </div>
            <div className="bg-laal h-15 rounded-2xl shadow shadow-mycolor flex flex-col items-center justify-center">
              <h1 className="font-myfamily text-xl">
                Total Expense: {balances[0]?.total_expense}${" "}
              </h1>
            </div>
          </div>
        </div>
      </section>

      <section className="graph mt-10">
        <div className="bg-white md:h-150 shadow-2xl shadow-[#A5B4FC] rounded-4xl flex flex-col items-center justify-center">
          <LineChart
            incomeData={incomeChartData}
            expenseData={expenseChartData}
            totalData={totalChartData}
          />
        </div>
      </section>
    </div>
  );
}

export default Dashboard;
