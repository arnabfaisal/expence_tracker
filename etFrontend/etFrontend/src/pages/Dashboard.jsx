import React, { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { useMemo } from "react";
import { userBalanceStore } from "../../store/userBalanceStore";
import { useTransactionStore } from "../../store/transitionStore";
import { handler } from "../../store/helper";
import LineChart from "../components/Linechart";

// Temporary mock data for the chart

function Dashboard() {
  const { balances, fetchbalances } = userBalanceStore();

  const { transactions, fetchtransactions } = useTransactionStore();
  // console.log(transactions);

  useEffect(() => {
    fetchbalances();
    fetchtransactions();

    const interval = setInterval(() => {
      fetchbalances();
      fetchtransactions();
    }, 10000); // every 10 seconds

    return () => clearInterval(interval);
  }, []);

  const result = useMemo(() => handler(0, transactions), [transactions]);

  const incomeChartData = result.incomeData;
  const expenseChartData = result.expenseData;
  const totalChartData = result.totalData;

  return (
    <div className="container max-w-6xl mx-auto px-4">
      <section className="twobuttons  mt-5">
        <div>
          <Button className="w-full mb-5 bg-asmani text-xl">
            Create a Transaction
          </Button>
        </div>
        <div>
          <Button className="w-full bg-asmani text-xl">Create a Goal</Button>
        </div>
      </section>

      <section className="summary mt-5">
        <div className="bg-white h-90 shadow-2xl shadow-[#A5B4FC] rounded-4xl">
          <div className="flex justify-between px-6">
            <div className="mt-5">
              <h1 className="text-2xl font-myfamily font-semibold">Summary</h1>
            </div>
            <div className="flex gap-4 mt-5">
              <Button className="bg-asmani md:text-xl text-[10px]">Your Goals</Button>
              <Button className="bg-asmani md:text-xl text-[8px]">Your Transactions</Button>
            </div>
          </div>

          <div className="flex flex-col w-full px-6 mt-6">
            <div className="bg-maati mt-5 mb-5 h-15 rounded-2xl flex flex-col items-center justify-center">
              <h1 className="font-myfamily text-xl">
                Total Balance: {balances[0]?.get_total_balance}${" "}
              </h1>
            </div>
            <div className="bg-shobuj mb-5 h-15 rounded-2xl flex flex-col items-center justify-center">
              <h1 className="font-myfamily text-xl">
                Total Income: {balances[0]?.total_income}${" "}
              </h1>
            </div>
            <div className="bg-laal h-15 rounded-2xl flex flex-col items-center justify-center">
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
