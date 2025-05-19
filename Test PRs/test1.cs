// C# Code Snippet for Code Review
// This class is intended to process orders, but contains several issues.

using System;
using System.Collections.Generic;
using System.Linq;

public class orderProcessor // Issue: Naming convention (should be PascalCase)
{
    // Issue: Public field, should ideally be a property with encapsulation
    public List<string> product_List; 
    private string customerName; // Issue: Not used
    private const double TaxRate = 0.08; // Good: const for fixed value

    // Constructor
    public orderProcessor()
    {
        product_List = new List<string>();
        // Issue: customerName is declared but never initialized or used meaningfully in this constructor
    }

    // Method to add a product
    // Issue: Method name doesn't follow PascalCase convention
    public void addProduct(string product) 
    {
        if (!String.IsNullOrEmpty(product)) // Good: Basic null/empty check
        {
            product_List.Add(product);
        }
        // Issue: No feedback if the product is null or empty (e.g., throw exception or return bool)
    }

    // Method to get the total price
    // Issue: Inefficient string concatenation in a loop
    // Issue: "Magic number" for price (10.0)
    // Issue: No error handling if product_List is null (though constructor initializes it)
    public string GetOrderSummaryAndTotalPrice()
    {
        string summary = "Order Summary: ";
        double total = 0;
        for (int i = 0; i < product_List.Count; i++) // Issue: Can use foreach for better readability
        {
            summary += product_List[i] + ", "; // Issue: Inefficient string concatenation
            total += 10.0; // Issue: Price is hardcoded (magic number)
        }

        total = total + (total * TaxRate); // Apply tax

        // Issue: Potential off-by-one in substring if list is empty, leading to ArgumentOutOfRangeException
        // Issue: If product_List is empty, summary will be "Order Summary: , " which is not ideal.
        // A better approach would be to use string.Join or a StringBuilder.
        if (product_List.Count > 0) {
            summary = summary.Substring(0, summary.Length - 2); // Remove trailing comma and space
        } else {
            summary = "No items in the order.";
        }
        
        return summary + ". Total Price: $" + total.ToString("F2");
    }

    // Method to process an order, but it's not fully implemented
    // Issue: Method is public but doesn't do anything useful yet.
    // Issue: Parameter 'discountCode' is not used.
    public bool ProcessOrder(string paymentType, string discountCode)
    {
        if (product_List.Count == 0)
        {
            Console.WriteLine("Cannot process an empty order."); // Issue: Console.WriteLine in a class library is often bad practice (should throw exception or return status)
            return false;
        }

        // TODO: Implement actual order processing logic (e.g., payment, inventory update)
        // Issue: "TODO" comments are fine, but this method returns true without doing much.
        
        // Issue: Hardcoded "Processed" status. What if processing fails?
        string status = "Processed"; 
        Console.WriteLine("Order status: " + status);

        return true; 
    }

    // Unused private method
    // Issue: Dead code
    private void LogOrderDetails(string orderId)
    {
        Console.WriteLine("Logging details for order: " + orderId);
        // This method is never called.
    }

    // Example of a method with a potential NullReferenceException
    public int GetFirstProductLength(List<string> products)
    {
        // Issue: No null check for the 'products' list itself before accessing it.
        // Issue: No check if 'products' is empty before accessing products[0].
        // This will throw NullReferenceException if 'products' is null,
        // or ArgumentOutOfRangeException if 'products' is empty.
        return products[0].Length; 
    }

    // Method with unclear purpose and potential issues
    public static void HelperUtility(int value, string data) // Issue: Static method in an instance class, might be better in a separate utility class
    {
        if (value > 100) // Issue: Magic number 100
        {
            // Perform some operation
            string result = ""; // Issue: Variable 'result' is assigned but its value is never used.
            for(int i=0; i<value; i+=5) // Issue: Loop condition and increment might not be obvious without context
            {
                // ... some complex logic missing ...
            }
        }
        // Issue: No return value, no clear side effects. What does this method do?
        // Issue: 'data' parameter is not used.
    }
}

// Example Usage (for context, not part of the reviewable class itself)
public class Program
{
    public static void Main(string[] args)
    {
        orderProcessor myOrder = new orderProcessor();
        myOrder.addProduct("Apple");
        myOrder.addProduct("Banana");
        myOrder.addProduct(""); // Test empty product add

        Console.WriteLine(myOrder.GetOrderSummaryAndTotalPrice());

        myOrder.ProcessOrder("CreditCard", "SAVE10");

        List<string> items = new List<string> { "Laptop", "Mouse" };
        // Console.WriteLine(myOrder.GetFirstProductLength(items)); // Works

        // List<string> emptyItems = new List<string>();
        // Console.WriteLine(myOrder.GetFirstProductLength(emptyItems)); // Will throw ArgumentOutOfRangeException

        // List<string> nullItems = null;
        // Console.WriteLine(myOrder.GetFirstProductLength(nullItems)); // Will throw NullReferenceException
        
        orderProcessor.HelperUtility(200, "test data");
    }
}
