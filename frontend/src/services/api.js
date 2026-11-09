
const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || "/api"
).replace(/\/+$/, "");

export async function checkApiHealth() {
  const response = await fetch(`${API_BASE_URL}/health`);

  if (!response.ok) {
    throw new Error("Unable to connect to the prediction service.");
  }

  return await response.json();
}

export async function predictDemand(inputData) {
  const controller = new AbortController();

  const timeout = setTimeout(() => {
    controller.abort();
  }, 60000);

  try {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(inputData),
      signal: controller.signal,
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(
        result.detail || "Demand prediction failed."
      );
    }

    if (typeof result.predicted_demand !== "number") {
      throw new Error("Invalid prediction received from the API.");
    }

    return result;
  } catch (error) {
    if (error.name === "AbortError") {
      throw new Error(
        "The prediction service took too long to respond. Please try again."
      );
    }

    throw error;
  } finally {
    clearTimeout(timeout);
  }
}
