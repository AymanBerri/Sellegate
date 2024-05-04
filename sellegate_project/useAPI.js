
import axios from "axios";
import useAuthStore from "../stores/userStore";

const useAPI = () => {
	const { id: userId, username } = useAuthStore();
	const API_URL = "http://localhost:3000"; // Don't worry about this, we will adjust it as necessary later...

	// TODO:
	// - adjust the backend to meet what i'm expecting (please if u can follow the same naming for the returned data, it will be much easier for me to integrate later)
	// - note, there are some parts that i need u to return an error message, please make the shape same for all. For example:
	// {
	//     status: ...
	//     error: {
	//         message: ..
	//     }
	//     // up to u to shape it..
	// }
	// - write the details for each function (the steps not code) for how can i use the backend to reach the results i want ( i dont care if u want me to write more than 1 call, its k but tell me how can i reach the response i need )
	// - if u finished everything, contact me to start working on how we can include images.. However, for now skip it

	const signup = async (signupData: SignupRequest): Promise<AuthResponse> => {
		// I'll send these values:
		// {username: string, email: string, password: string}
		//
		// And u should create a new user and return it with the token. Note how the response should be:
		// {
		//     id: ...
		//     username: ...
		//     email: ...
		//     isEvalutor: false // THIS WILL BE SET AS FALSE FROM UR SIDE ALWAYS
		//     token: ...
		//     evaluatorProfile: { // I dont care how u wanna store this, but im pretty sure u can store it somehow and group all the data in a single response object matches what i'm expecting
		//         bio: "" // THIS WILL BE SET AS EMPTY STRING FROM UR SIDE
		//         // currently the evalutor profile inculde a bio only... we may add later, but most likely we wont...
		//     }
		// }
	};

	const login = async (loginData: LoginRequest): Promise<AuthResponse> => {
		// I'll send these values:
		// {email: string, password: string}
		//
		// And u should return the user data if it exist with the new token:
		// {
		//     id: ...
		//     username: ...
		//     email: ...
		//     isEvalutor: ...
		//     token: ...
		//     evaluatorProfile: {
		//         bio: ...
		//     }
		// }
		//
		// otherwise, if the email or password is wrong, return an error with the appropriate message
	};

	const getUserProfile = async (userId: string): Promise<AuthResponse> => {
		// Here, i'll call an endpoint (name it whatever) and u should return the user data according to the header token
		// the user data:
		// {
		//     id: ...
		//     username: ...
		//     email: ...
		//     isEvalutor: ...
		//     token: ...
		//     evaluatorProfile: {
		//         bio: ...
		//     }
		// }
		//
		// if the token is invalid or so, return an appropriate error message
	};

	const updateUser = async (userId: string, values: Partial<AuthResponse>): Promise<void> => {
		// Here, ill send a PATCH command for the current logged in user (the header token) on a X endpoint (name it whatever) and u should update all the user values according to what i sent
		// the excepted values (note i may send some of them, or all of them, and they will be in this shape):
		// {
		//     username: ...
		//     email: ...
		//     evaluatorProfile: {
		//         bio: ...
		//     }
		// }
		//
		// a body example would be like:
		// {
		// 	    evaluatorProfile: {
		// 		    bio: "Here's my new bio!!";
		//  	}
		// }
	};

	const getAllItems = async (): Promise<ItemResponse[]> => {
		// here just return all the existing items, make sure they are in this shape:
		// {
		//     id: string;
		//     name: string;
		//     imgUrl: string OR null; // for now keep it (null always)
		//     description: string;
		//     price: number;
		//     sellerId: string;
		//     sellerName: string; // I dont care how u store it, return it with the response, or guide me what should i call to reach this shape
		//     createdAt: string; // for all createdAt, i just care about the date. Use any format.. ex: 2024/4/3
		//     isSold: boolean;
		//     delegationState: "Independent" OR "Pending" OR "Approved" OR "Rejected";
		//     evaluatorId: string OR null; // if its evaluted it should contain the evalutor id, otherwise it should be null
		// }
	};

	const getItemsToExplore = async (): Promise<ItemResponse[]> => {
		// name the endpoint as u want...
		// here just return all the existing items that are NOT owned by the current user (so fillter them according to the token), make sure they are in this shape:
		// {
		//     id: string;
		//     name: string;
		//     imgUrl: string OR null; // for now keep it (null always)
		//     description: string;
		//     price: number;
		//     sellerId: string;
		//     sellerName: string; // I dont care how u store it, return it with the response, or guide me what should i call to reach this shape
		//     createdAt: string;
		//     isSold: boolean;
		//     delegationState: "Independent" OR "Pending" OR "Approved" OR "Rejected";
		//     evaluatorId: string OR null; // if its evaluted it should contain the evalutor id, otherwise it should be null
		// }
	};

	const getItem = async (itemId: string): Promise<ItemResponse> => {
		// here ill call an endpoint could be named whatever, and ill include the ID in the endpoint (e.g., `items/123` ). And u should return an item in this shape:
		// {
		//     id: string;
		//     name: string;
		//     imgUrl: string OR null; // for now keep it (null always)
		//     description: string;
		//     price: number;
		//     sellerId: string;
		//     sellerName: string; // I dont care how u store it, return it with the response, or guide me what should i call to reach this shape
		//     createdAt: string;
		//     isSold: boolean;
		//     delegationState: "Independent" OR "Pending" OR "Approved" OR "Rejected";
		//     evaluatorId: string OR null; // if its evaluted it should contain the evalutor id, otherwise it should be null
		// }
	};

	const getUserProducts = async (): Promise<ItemResponse[]> => {
		// here just return all the existing items that are OWNED by the current user (so fillter them according to the token), make sure they are in this shape:
		// {
		//     id: string;
		//     name: string;
		//     imgUrl: string OR null; // for now keep it (null always)
		//     description: string;
		//     price: number;
		//     sellerId: string;
		//     sellerName: string; // I dont care how u store it, return it with the response, or guide me what should i call to reach this shape
		//     createdAt: string;
		//     isSold: boolean;
		//     delegationState: "Independent" OR "Pending" OR "Approved" OR "Rejected";
		//     evaluatorId: string OR null; // if its evaluted it should contain the evalutor id, otherwise it should be null
		// }
	};

	const postItem = async (item: ItemRequest): Promise<void> => {
		// here ill send u these values
		//
		// {
		//     name: string;
		//     imgUrl: null OR Image; // I'm assuming i can send u an image file here, however, currently ill be sending null always, so u may check if its null set it as null, if its file object or image, store it or so.. if its hard skip it and make it null always
		//     description: string;
		//     price: number;
		//     delegationState: "Independent" OR "Pending" OR "Approved" OR "Rejected"; // I'll send u one of the 4 states
		// }
		//
		// and u should create a new item that looks like this for example (dont return it, but if i later tried to get it, it should be like this):
		//
		// {
		//     id: ...; // U SET IT
		//     name: string;
		//     imgUrl: null OR Image; // NULL FOR NOW
		//     description: string;
		//     price: number;
		//     sellerId: ...; // USE THE TOKEN TO GET THE ID
		//     sellerName: string; // u may not need to store it, but later ofc ill need u to return it somehow on getItem
		//     createdAt: string;
		//     isSold: boolean; // FALSE BY DEFAULT
		//     delegationState: "Independent" OR "Pending" OR "Approved" OR "Rejected";
		//     evaluatorId: string OR null; // NULL BY DEFAULT
		// }
	};

	const updateItem = async (itemId: string, values: Partial<ItemRequest>): Promise<void> => {
		// Here, ill send a PATCH command for the current logged in user (the header token) on a X endpoint (name it whatever) and u should update all the ITEM values according to what i sent
		// Note, u have to check if the current logged in user own this item or not (by using sellerId) if not, return an error message
		// the excepted values (note i may send some of them, or all of them, and they will be in this shape):
		// {
		//     name: string;
		//     imgUrl: null OR Image;
		//     description: string;
		//     price: number;
		//     delegationState: "Independent" OR "Pending" OR "Approved" OR "Rejected";
		// }
	};

	const deleteItem = async (itemId: string): Promise<void> => {
		// Delete the item on DELETE command for endpoint that looks like `item/123`. Make sure that the current logged in user is OWNNING the item, otherwise return an error message
	};

	const buyItem = async (itemId: string): Promise<void> => {
		// here, ill call endpoint `items/123/buy` (or whatever it named). And u must check if its a valid item to buy
		// - isSold should be false
		// - sellerId should be not owned by the current logged in user
		// if its valid, buy it and create a new record or data for this payment. The shape of the respones of this payment if i tried to get it later should be like this (not, the RESPONES not how u store it...):
		// {
		//     id: string,
		//     itemId: string,
		//     userId: string,
		//     itemName: string,
		//     totalPrice: number,
		//     createdAt: string,
		// };
		//
		// the above shape for example, dont return it
	};

	const getUserPayments = async (): Promise<PaymentResponse[]> => {
		// here, ill call endpoint `payments` (or whatever it named). And u must return all the payments for the current logged in user (token)
		// response shape:
		// {
		//     id: string,
		//     itemId: string,
		//     userId: string,
		//     itemName: string,
		//     totalPrice: number,
		//     createdAt: string,
		// };
	};

	const sendAssessmentRequest = async (assessmentRequest: AssessmentRequest): Promise<void> => {
		// NOTE: u must ensure the current user isEvaluator (otherwise prevet this, and return an error message)
		// here, ill call an endpoint `assessment` or whatever, as POST method. and ill send these values (up to u how to store them):
		// {
		//     itemId: string;
		//     name: string; // which will be the title of the message
		//     message: string;
		//     price: number; // which is the new estimated price
		// }
		//
		// NOTE, for better understanding the assessment should look like this as an object of i retrive it now (instantly after creating it):
		// {
		//     id: string, // YOU CREATE IT
		//     itemId: string,
		//     evaluatorId: string, // USE THE CURRENT LOGGED IN USER ID
		//     name: string,
		//     message: string,
		//     price: string,
		//     state: string, // ON FIRST CREATION, ALWAYS SET IT TO: "Pending" === Note the possible valus here are 3, which're: "Pending" OR "Approved" OR "Rejected"
		//     createdAt: string,
		// }
	};

	const getMyAssessments = async (): Promise<AssessmentResponse[]> => {
		// NOTE: u must ensure the current user isEvaluator (otherwise prevet this, and return an error message)
		// return all current user assessmnt requests in this shape:
		// {
		//     id: string;
		//     itemId: string;
		//     evaluatorId: string;
		//     name: string;
		//     message: string;
		//     price: number;
		//     state: "Pending" OR "Approved" OR "Rejected";
		//     createdAt: string;
		// }
	};

	const getAssessmentRequestsOnMyProduct = async (productId: string): Promise<AssessmentResponse[]> => {
		// Here, the user ill call an endpoint X (name it whatever u want), and u should return all the assessments for the current user and its item
		// So, ill send u only this in the body:
		// { itemId: string }
		// u must check the following:
		// - the itemId is realy owned by the current logged In user
		// - and then retrive all assessments for this user for this particular item (the filltering up to u)
		// Response Shape:
		// {
		//     id: string;
		//     itemId: string;
		//     evaluatorId: string;
		//     name: string;
		//     message: string;
		//     price: number;
		//     state: "Pending" OR "Approved" OR "Rejected";
		//     createdAt: string;
		// }
	};

	const rejectAssessment = async (assessmentId: string): Promise<void> => {
		// here, ill send u a PATCH command to modify assessment on user item. Name the endpoint as u wish, maybe: assessment/213/reject
		// So do the following
		// - check the current user is owning the itemId for the assessment he want to reject (otherwise error message)
		// - update the state to "Rejected"
		//
		// Don't return anything, however, if i later on tried to get the assessment it should look like this:
		// {
		//     id: ...;
		//     itemId: ...;
		//     evaluatorId: ...;
		//     name: ...;
		//     message: ...;
		//     price: ...;
		//     state: "Rejected";
		//     createdAt: ...;
		// }
	};

	const acceptAssessment = async (assessmentId: string): Promise<void> => {
		// here, ill send u a PATCH command to modify assessment on user item. Name the endpoint as u wish, maybe: assessment/213/accept
		// So do the following
		// - check the current user is owning the itemId for the assessment he want to accept (otherwise error message)
		// - update the state to "Approved"
		//
		// Don't return anything, however, if i later on tried to get the assessment it should look like this:
		// {
		//     id: ...;
		//     itemId: ...;
		//     evaluatorId: ...;
		//     name: ...;
		//     message: ...;
		//     price: ...;
		//     state: "Approved";
		//     createdAt: ...;
		// }
	};

	return {
		signup,
		login,
		getUserProfile,
		updateUser,
		getAllItems,
		getItemsToExplore,
		getItem,
		getUserProducts,
		postItem,
		updateItem,
		deleteItem,
		buyItem,
		getUserPayments,
		sendAssessmentRequest,
		getMyAssessments,
		getAssessmentRequestsOnMyProduct,
		rejectAssessment,
		acceptAssessment,
	};
};

// YOU SHOULD NOT CARE ABOUT ANYTHING BELOW...

interface SignupRequest {
	username: string;
	email: string;
	password: string;
}

interface LoginRequest {
	email: string;
	password: string;
}

export interface AuthResponse {
	id: string;
	username: string;
	email: string;
	token: string;
	isEvaluator: boolean;
	evaluatorProfile: { bio: string }; // we can add more fields later...
}

export interface PaymentResponse {
	id: string;
	itemId: string;
	itemName: string;
	userId: string;
	totalPrice: number;
	createdAt: string;
}

export interface ItemRequest {
	name: string;
	imgUrl: string | null;
	description: string;
	price: number;
	delegationState: DelegationStates;

	isSold?: boolean; // This is temp solution, i should delete it when i integrate with the real backend
}

export interface ItemResponse {
	id: string;
	name: string;
	imgUrl: string | null;
	description: string;
	price: number;
	sellerId: string;
	sellerName: string;
	createdAt: string;
	isSold: boolean;
	delegationState: DelegationStates;
	evaluatorId: string | null;
}

export interface AssessmentRequest {
	itemId: string;
	name: string;
	message: string;
	price: number;
}

export interface AssessmentResponse {
	id: string;
	itemId: string;
	evaluatorId: string;
	name: string;
	message: string;
	price: number;
	state: DelegationStates;
	createdAt: string;
}

export enum DelegationStates {
	INDEPENDENT = "Independent",
	PENDING = "Pending",
	APPROVED = "Approved",
	REJECTED = "Rejected",
}

export enum ItemStates {
	FOR_SALE = "For Sale",
	SOLD = "Sold",
}
