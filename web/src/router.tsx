import { createBrowserRouter } from "react-router-dom";

import { 
  ErrorPage,
  CreateAccountPage,
  HomePage,
  OpenChatChatPage
} from "./pages";
import { 
  createAccountPath, 
  homePath,
  openChatPath
} from "./lib/paths";


const router = createBrowserRouter([
  {
    path: homePath,
    element: <HomePage />,
    errorElement: <ErrorPage />,
  },
  {
    path: createAccountPath,
    element: <CreateAccountPage />,
    errorElement: <ErrorPage />,
  },
  {
    path: openChatPath,
    element: <OpenChatChatPage />,
    errorElement: <ErrorPage />,
  },
]);

export default router;