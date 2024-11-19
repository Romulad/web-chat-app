import { createBrowserRouter } from "react-router-dom";

import { 
  ErrorPage,
  HomePage,
  OpenChatChatPage,
  OpenChatPage,
} from "./pages";
import { 
  homePath,
  openChatHomePath,
  openChatPath
} from "./lib/paths";


const router = createBrowserRouter([
  {
    path: homePath,
    element: <HomePage />,
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