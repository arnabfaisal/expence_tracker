import React, { useEffect , useState} from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";




import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

import { useTransactionStore } from "../../store/transitionStore";
import { Skeleton } from "@/components/ui/skeleton";

import TransactionCard from "../components/ui/TransactionCard";

function Transaction() {
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  const [formDataTx, setFormDataTx] = useState({
    category_id: 0,
    amount: "",
    description: "",
    transaction_type: "",
  });
  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormDataTx((prev) => ({
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
    } catch (error) {
      console.log("failed....");
    }
    setFormDataTx({
      category_id: 0,
      amount: "",
      description: "",
      transaction_type: "",
    });
  };

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
                    htmlFor="description"
                    className="mb-1 font-medium myfamily text-gray-800"
                  >
                    description
                  </label>
                  <input
                    id="description"
                    type="text"
                    placeholder="description"
                    className="border text-gray-800 border-mycolor rounded-2xl px-3 py-2 focus:outline-none focus:ring-mycolor bg-gray-100"
                    name="description"
                    value={formDataTx.description}
                    onChange={handleChange}
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
                    htmlFor="category"
                    className="mb-1 font-medium myfamily text-gray-800"
                  >
                    Category
                  </label>
                  <input
                    id="category_id"
                    type="number"
                    placeholder="category_id"
                    className="border text-gray-800 border-mycolor rounded-2xl px-3 py-2 focus:outline-none focus:ring-mycolor bg-gray-100"
                    name="category_id"
                    value={formDataTx.category_id}
                    onChange={handleChange}
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
