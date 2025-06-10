import React, { useEffect } from "react";
import { Button } from "@/components/ui/button";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

import { useTransactionStore } from "../../store/transitionStore";
import { Skeleton } from "@/components/ui/skeleton";

import TransactionCard from "../components/ui/TransactionCard";

function Transaction() {
  const { loading, transactions, fetchtransactions } = useTransactionStore();
  console.log(transactions);

  const incomeTransactions = transactions.filter(
    (transaction) => transaction.transaction_type === "income"
  );
  const expenseTransactions = transactions.filter(
    (transaction) => transaction.transaction_type === "expense"
  );

  useEffect(() => {
    fetchtransactions();

    const interval = setInterval(() => {
      fetchtransactions();
    }, 1000000); // every 10 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="container max-w-6xl mx-auto px-4 min-h-screen">
      <div>
        <Button className="bg-asmani w-full md:text-xl border border-purple-600">
          Creata a Transaction
        </Button>
      </div>

      <div className="flex flex-col mt-10 items-center">
        <h1 className="text-4xl mb-5">Transactions</h1>
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
            </TabsList>
            <TabsContent
              value="All"
              className="w-full grid grid-cols-1 md:grid-cols-3 gap-y-6 justify-items-center"
            >
              {transactions.map((transaction) => (
                <TransactionCard
                  key={transaction.id}
                  transaction={transaction}
                />
              ))}
            </TabsContent>
            <TabsContent
              value="Income"
              className="w-full grid grid-cols-1 md:grid-cols-3 gap-y-6 justify-items-center"
            >
              {incomeTransactions.map((transaction) => (
                <TransactionCard
                  key={transaction.id}
                  transaction={transaction}
                />
              ))}
            </TabsContent>
            <TabsContent
              value="Expense"
              className="w-full grid grid-cols-1 md:grid-cols-3 gap-y-6 justify-items-center"
            >
              {expenseTransactions.map((transaction) => (
                <TransactionCard
                  key={transaction.id}
                  transaction={transaction}
                />
              ))}
            </TabsContent>
          </Tabs>
        )}
      </div>
    </div>
  );
}

export default Transaction;
