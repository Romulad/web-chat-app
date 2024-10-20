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
  openChatHomePath,
  openChatPath
} from "./lib/paths";
import OpenChatPage from "./pages/openChatPage";


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
  {
    path: openChatHomePath,
    element: <OpenChatPage />,
    errorElement: <ErrorPage />,
  },
]);

export default router;