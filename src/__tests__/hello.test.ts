import { render, screen } from "@testing-library/svelte";
import App from "../App.svelte";

test("should render", () => {
  render(App);
  const node = screen.queryByText("Software Lifecycle Environmental Impact");
  expect(node).not.toBeNull();
});

